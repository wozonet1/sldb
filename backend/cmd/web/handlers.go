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

// predictHandler 实现了与Python代码完全相同的接口逻辑。
func (app *application) predictHandler(c *gin.Context) {
	geneA := c.Query("geneA")
	geneB := c.Query("geneB")

	if geneA == "" {
		app.clientError(c, http.StatusBadRequest, "Gene A is required")
		return
	}

	// --- 场景一: 查询特定基因对 ---
	if geneB != "" {
		p, err := app.predictions.GetOne(geneA, geneB)
		if err != nil {
			if errors.Is(err, mysql.ErrNoRecord) {
				app.notFound(c)
			} else {
				app.serverError(c, err)
			}
			return
		}

		// 转换为对外的响应结构
		resp := models.PredictionResponse{
			GeneA:              p.GeneA,
			GeneB:              p.GeneB,
			PredictionScore:    p.PredictionScore,
			PredictingRelation: p.PredictingRelation,
		}
		c.JSON(http.StatusOK, resp)
		return
	}

	// --- 场景二: 查询与单个基因相关的所有记录，并进行排序筛选 ---
	allRecords, err := app.predictions.GetAllForGeneA(geneA)
	if err != nil {
		app.serverError(c, err)
		return
	}

	if len(allRecords) == 0 {
		app.notFound(c)
		return
	}

	// 内存中筛选和排序逻辑
	var priorityRecords []*models.Prediction
	var remainingRecords []*models.Prediction

	for _, r := range allRecords {
		if r.BinaryPrediction == 1 && r.Label == "old_SL" {
			priorityRecords = append(priorityRecords, r)
		} else if r.BinaryPrediction == 1 {
			remainingRecords = append(remainingRecords, r)
		}
	}

	var combinedRecords []*models.Prediction
	numPriority := len(priorityRecords)

	if numPriority < 20 && len(remainingRecords) > 0 {
		needed := 20 - numPriority
		if needed > len(remainingRecords) {
			needed = len(remainingRecords)
		}
		// Go没有内置的random.sample，我们自己实现一个简单的随机选择
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

	// 按预测分数降序排列
	sort.Slice(combinedRecords, func(i, j int) bool {
		return combinedRecords[i].PredictionScore > combinedRecords[j].PredictionScore
	})

	// 转换为对外的响应结构列表
	var finalResponse []models.PredictionResponse
	for _, p := range combinedRecords {
		finalResponse = append(finalResponse, models.PredictionResponse{
			GeneA:              p.GeneA,
			GeneB:              p.GeneB,
			PredictionScore:    p.PredictionScore,
			PredictingRelation: p.PredictingRelation,
		})
	}

	c.JSON(http.StatusOK, finalResponse)
}
