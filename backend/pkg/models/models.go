// file: pkg/models/models.go
package models

import "database/sql"

// GoAnnotation 代表一个GO注释条目。
type GoAnnotation struct {
	ID          string `json:"id"`
	Description string `json:"description"`
}

// GeneInfo 代表一个基因及其所有关联的GO注释。
type GeneInfo struct {
	Symbol      string          `json:"symbol"`
	Annotations []*GoAnnotation `json:"annotations"`
}

// PredictionResponse 是最终返回给前端的、包含丰富信息的预测结果结构。
type PredictionResponse struct {
	GeneA           *GeneInfo `json:"geneA"`
	GeneB           *GeneInfo `json:"geneB"`
	PredictionScore float64   `json:"predictionScore"`
	Label           string    `json:"label"`
	GseSource       *string   `json:"gseSource"` // 使用指针处理可能的NULL值
	GseData         *string   `json:"gseData"`
}

type FlatDBResult struct {
	GeneASymbol     string
	GeneBSymbol     string
	PredictionScore float64
	Label           string
	GseSource       sql.NullString
	GseData         sql.NullString

	BinaryPrediction int // <-- 新增此字段，用于内部排序逻辑

	// GO注释相关字段
	GeneAGoID          sql.NullString
	GeneAGoDescription sql.NullString
	GeneBGoID          sql.NullString
	GeneBGoDescription sql.NullString
}
