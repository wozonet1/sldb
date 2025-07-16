// file: cmd/web/handlers.go
package main

import (
	"errors"
	"math/rand"
	"net/http"
	"sort"

	"geneprediction.wozonet.net/pkg/models"
	"geneprediction.wozonet.net/pkg/models/mysql"
	"github.com/gin-gonic/gin"
)

func (app *application) predictHandler(c *gin.Context) {
	// 注意：我们从现在起将用户查询的基因称为 queryGene
	queryGene := c.Query("geneA")
	partnerGene := c.Query("geneB")

	if queryGene == "" {
		app.clientError(c, http.StatusBadRequest, "Gene A symbol is required")
		return
	}

	// --- 场景一: 查询特定基因对 (partnerGene不为空) ---
	if partnerGene != "" {
		flatResults, err := app.predictions.GetByGenePair(queryGene, partnerGene)
		if err != nil {
			if errors.Is(err, mysql.ErrNoRecord) {
				app.notFound(c)
			} else {
				app.serverError(c, err)
			}
			return
		}
		response := buildNestedResponse(flatResults)

		// --- [新增调整逻辑] ---
		// 确保返回的JSON中，geneA字段始终是用户查询的第一个基因
		if response.GeneA.Symbol != queryGene {
			response.GeneA, response.GeneB = response.GeneB, response.GeneA
		}
		// --- [新增调整逻辑结束] ---

		c.JSON(http.StatusOK, response)
		return
	}

	// --- 场景二: 查询与单个基因相关的所有记录 (partnerGene为空) ---
	allFlatResults, err := app.predictions.GetAllForGeneSymbol(queryGene)
	if err != nil {
		if errors.Is(err, mysql.ErrNoRecord) {
			c.JSON(http.StatusOK, []models.PredictionResponse{})
			return
		}
		app.serverError(c, err)
		return
	}

	allParsedRecords := buildNestedResponseList(allFlatResults)

	// --- [核心修改] ---
	// 遍历所有聚合好的记录，确保每一条记录的 GeneA 字段都是用户查询的那个基因
	for _, record := range allParsedRecords {
		if record.GeneA.Symbol != queryGene {
			record.GeneA, record.GeneB = record.GeneB, record.GeneA
		}
	}
	// --- [核心修改结束] ---

	// --- 执行筛选、抽样和排序逻辑 (与之前类似，但现在操作的是调整过顺序的列表) ---
	var priorityRecords []*models.PredictionResponse
	var remainingRecords []*models.PredictionResponse

	for _, r := range allParsedRecords {
		// 假设Python代码中的 `BinaryPrediction == 1` 是筛选高可信度结果
		// 我们可以通过Label来模拟这个筛选逻辑
		isHighConfidence := r.Label == "old_SL" || r.Label == "new_SL"

		if isHighConfidence && r.Label == "old_SL" {
			priorityRecords = append(priorityRecords, r)
		} else if isHighConfidence {
			remainingRecords = append(remainingRecords, r)
		}
	}

	var combinedRecords []*models.PredictionResponse
	numPriority := len(priorityRecords)

	if numPriority < 20 && len(remainingRecords) > 0 {
		needed := 20 - numPriority
		if needed > len(remainingRecords) {
			needed = len(remainingRecords)
		}
		rand.Shuffle(len(remainingRecords), func(i, j int) {
			remainingRecords[i], remainingRecords[j] = remainingRecords[j], remainingRecords[i]
		})
		remainingSample := remainingRecords[:needed]
		combinedRecords = append(priorityRecords, remainingSample...)
	} else {
		if numPriority > 20 {
			numPriority = 20
		}
		combinedRecords = priorityRecords[:numPriority]
	}

	sort.Slice(combinedRecords, func(i, j int) bool {
		return combinedRecords[i].PredictionScore > combinedRecords[j].PredictionScore
	})

	c.JSON(http.StatusOK, combinedRecords)
}

// (buildNestedResponse 函数保持不变)
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

	if firstRow.GseSource.Valid {
		response.GseSource = &firstRow.GseSource.String
	}
	if firstRow.GseData.Valid {
		response.GseData = &firstRow.GseData.String
	}

	geneAAnnotations := make(map[string]string)
	geneBAnnotations := make(map[string]string)

	for _, row := range flatResults {
		if row.GeneAGoID.Valid {
			if row.GeneASymbol == response.GeneA.Symbol {
				geneAAnnotations[row.GeneAGoID.String] = row.GeneAGoDescription.String
			} else {
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

	for id, desc := range geneAAnnotations {
		response.GeneA.Annotations = append(response.GeneA.Annotations, &models.GoAnnotation{ID: id, Description: desc})
	}
	for id, desc := range geneBAnnotations {
		response.GeneB.Annotations = append(response.GeneB.Annotations, &models.GoAnnotation{ID: id, Description: desc})
	}

	return response
}

// (buildNestedResponseList 函数保持不变)
func buildNestedResponseList(flatResults []*models.FlatDBResult) []*models.PredictionResponse {
	predictionMap := make(map[string]*models.PredictionResponse)

	for _, row := range flatResults {
		key := ""
		if row.GeneASymbol < row.GeneBSymbol {
			key = row.GeneASymbol + ":" + row.GeneBSymbol
		} else {
			key = row.GeneBSymbol + ":" + row.GeneASymbol
		}

		if _, exists := predictionMap[key]; !exists {
			response := &models.PredictionResponse{
				PredictionScore: row.PredictionScore,
				Label:           row.Label,
				GeneA: &models.GeneInfo{
					Symbol:      row.GeneASymbol,
					Annotations: []*models.GoAnnotation{},
				},
				GeneB: &models.GeneInfo{
					Symbol:      row.GeneBSymbol,
					Annotations: []*models.GoAnnotation{},
				},
			}
			if row.GseSource.Valid {
				response.GseSource = &row.GseSource.String
			}
			if row.GseData.Valid {
				response.GseData = &row.GseData.String
			}
			predictionMap[key] = response
		}
	}

	for _, row := range flatResults {
		key := ""
		if row.GeneASymbol < row.GeneBSymbol {
			key = row.GeneASymbol + ":" + row.GeneBSymbol
		} else {
			key = row.GeneBSymbol + ":" + row.GeneASymbol
		}
		resp := predictionMap[key]

		if row.GeneAGoID.Valid {
			resp.GeneA.Annotations = append(resp.GeneA.Annotations, &models.GoAnnotation{ID: row.GeneAGoID.String, Description: row.GeneAGoDescription.String})
		}
		if row.GeneBGoID.Valid {
			resp.GeneB.Annotations = append(resp.GeneB.Annotations, &models.GoAnnotation{ID: row.GeneBGoID.String, Description: row.GeneBGoDescription.String})
		}
	}

	var finalResponseList []*models.PredictionResponse
	for _, resp := range predictionMap {
		resp.GeneA.Annotations = uniqueAnnotations(resp.GeneA.Annotations)
		resp.GeneB.Annotations = uniqueAnnotations(resp.GeneB.Annotations)
		finalResponseList = append(finalResponseList, resp)
	}

	return finalResponseList
}

// (uniqueAnnotations 函数保持不变)
func uniqueAnnotations(annotations []*models.GoAnnotation) []*models.GoAnnotation {
	keys := make(map[string]bool)
	var list []*models.GoAnnotation
	for _, entry := range annotations {
		if _, value := keys[entry.ID]; !value {
			keys[entry.ID] = true
			list = append(list, entry)
		}
	}
	return list
}
