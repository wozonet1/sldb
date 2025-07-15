// file: cmd/web/handlers.go
package main

import (
	"errors"
	"net/http"

	"geneprediction.wozonet.net/pkg/models"       // 使用您的模块路径
	"geneprediction.wozonet.net/pkg/models/mysql" // 使用您的模块路径
	"github.com/gin-gonic/gin"
)

func (app *application) predictHandler(c *gin.Context) {
	geneA := c.Query("geneA")
	geneB := c.Query("geneB")

	if geneA == "" {
		app.clientError(c, http.StatusBadRequest, "Gene A symbol is required")
		return
	}

	if geneB == "" {
		// 在这个新版本中，我们只实现了查询基因对的逻辑
		// 如果需要实现只查单个基因的功能，可以在此扩展
		app.clientError(c, http.StatusBadRequest, "Gene B symbol is also required for this endpoint version")
		return
	}

	// 调用新的数据库查询方法
	flatResults, err := app.predictions.GetByGenePair(geneA, geneB)
	if err != nil {
		if errors.Is(err, mysql.ErrNoRecord) {
			app.notFound(c) // 使用辅助函数返回404
		} else {
			app.serverError(c, err) // 使用辅助函数返回500
		}
		return
	}

	// 调用辅助函数，将扁平数据转换为嵌套JSON
	response := buildNestedResponse(flatResults)

	c.JSON(http.StatusOK, response)
}

// buildNestedResponse 是一个辅助函数，用于聚合扁平的数据库查询结果。
func buildNestedResponse(flatResults []*models.FlatDBResult) *models.PredictionResponse {
	if len(flatResults) == 0 {
		return nil
	}

	firstRow := flatResults[0]
	response := &models.PredictionResponse{
		PredictionScore: firstRow.PredictionScore,
		Label:           firstRow.Label,
		GeneA: &models.GeneInfo{
			Symbol:      firstRow.GeneASymbol,
			Annotations: []*models.GoAnnotation{},
		},
		GeneB: &models.GeneInfo{
			Symbol:      firstRow.GeneBSymbol,
			Annotations: []*models.GoAnnotation{},
		},
	}

	// 处理可能为NULL的GSE字段
	if firstRow.GseSource.Valid {
		response.GseSource = &firstRow.GseSource.String
	}
	if firstRow.GseData.Valid {
		response.GseData = &firstRow.GseData.String
	}

	// 使用map来自动处理GO注释的去重
	geneAAnnotations := make(map[string]string)
	geneBAnnotations := make(map[string]string)

	for _, row := range flatResults {
		if row.GeneAGoID.Valid {
			// 确保我们只添加与正确的GeneA Symbol关联的注释
			if row.GeneASymbol == response.GeneA.Symbol {
				geneAAnnotations[row.GeneAGoID.String] = row.GeneAGoDescription.String
			} else { // 这对应于查询时A,B顺序颠倒的情况
				geneBAnnotations[row.GeneAGoID.String] = row.GeneAGoDescription.String
			}
		}
		if row.GeneBGoID.Valid {
			if row.GeneBSymbol == response.GeneB.Symbol {
				geneBAnnotations[row.GeneBGoID.String] = row.GeneBGoDescription.String
			} else {
				geneAAnnotations[row.GeneBGoID.String] = row.GeneBGoDescription.String
			}
		}
	}

	// 将去重后的map转换为最终的切片
	for id, desc := range geneAAnnotations {
		response.GeneA.Annotations = append(response.GeneA.Annotations, &models.GoAnnotation{ID: id, Description: desc})
	}
	for id, desc := range geneBAnnotations {
		response.GeneB.Annotations = append(response.GeneB.Annotations, &models.GoAnnotation{ID: id, Description: desc})
	}

	return response
}
