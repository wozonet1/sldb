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

// FlatDBResult 是一个临时的内部结构体，用于方便地从数据库的扁平化查询结果中扫描数据。
type FlatDBResult struct {
	GeneASymbol     string
	GeneBSymbol     string
	PredictionScore float64
	Label           string
	GseSource       sql.NullString
	GseData         sql.NullString

	GeneAGoID          sql.NullString
	GeneAGoDescription sql.NullString
	GeneBGoID          sql.NullString
	GeneBGoDescription sql.NullString
}
