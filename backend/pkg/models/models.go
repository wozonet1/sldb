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
// 这将是我们将要构建并返回给前端的最终JSON对象。
type PredictionResponse struct {
	GeneA           *GeneInfo `json:"geneA"`
	GeneB           *GeneInfo `json:"geneB"`
	PredictionScore float64   `json:"predictionScore"`
	Label           string    `json:"label"` // 预测来源
	GseSource       *string   `json:"gseSource"`
}

// FlatDBResult 是一个临时的内部结构体，用于方便地从数据库的扁平化查询结果中扫描数据。
// 我们从数据库中查出这样的扁平结构，然后在Go代码中将其组装成嵌套的 PredictionResponse。
type FlatDBResult struct {
	GeneASymbol     string
	GeneBSymbol     string
	PredictionScore float64
	Label           string
	GseSource       sql.NullString // 使用 sql.NullString 处理可能为NULL的GSE字段

	// GO注释相关字段，这些可能为NULL
	GeneAGoID          sql.NullString
	GeneAGoDescription sql.NullString
	GeneBGoID          sql.NullString
	GeneBGoDescription sql.NullString
}
