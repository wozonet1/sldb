// file: pkg/models/mysql/predictions.go
package mysql

import (
	"database/sql"
	"errors"

	"geneprediction.wozonet.net/pkg/models"
)

var ErrNoRecord = errors.New("models: no matching record found")

type PredictionModel struct {
	DB *sql.DB
}

// GetByGenePair 查询特定基因对的预测记录，并包含它们的GO注释 (此函数保持不变)
func (m *PredictionModel) GetByGenePair(geneASymbol, geneBSymbol string) ([]*models.FlatDBResult, error) {
	var geneAId, geneBId int

	stmtId := `SELECT symbol, gene_id FROM genes WHERE symbol IN (?, ?)`
	rowsId, err := m.DB.Query(stmtId, geneASymbol, geneBSymbol)
	if err != nil {
		return nil, err
	}
	defer rowsId.Close()

	idMap := make(map[string]int)
	for rowsId.Next() {
		var symbol string
		var id int
		if err := rowsId.Scan(&symbol, &id); err != nil {
			return nil, err
		}
		idMap[symbol] = id
	}

	var okA, okB bool
	geneAId, okA = idMap[geneASymbol]
	geneBId, okB = idMap[geneBSymbol]
	if !okA || !okB {
		return nil, ErrNoRecord
	}

	if geneAId > geneBId {
		geneAId, geneBId = geneBId, geneAId
	}

	stmt := `
        SELECT
            gA.symbol AS gene_a_symbol, gB.symbol AS gene_b_symbol,
            p.prediction_score, p.label, p.gse_source, p.gse_data,
            goA.go_id AS gene_a_go_id, goA.description AS gene_a_go_description,
            goB.go_id AS gene_b_go_id, goB.description AS gene_b_go_description
        FROM predictions p
        JOIN genes gA ON p.gene_a_id = gA.gene_id
        JOIN genes gB ON p.gene_b_id = gB.gene_id
        LEFT JOIN gene_go_mapping ggmA ON p.gene_a_id = ggmA.gene_id
        LEFT JOIN go_annotations goA ON ggmA.go_id = goA.go_id
        LEFT JOIN gene_go_mapping ggmB ON p.gene_b_id = ggmB.gene_id
        LEFT JOIN go_annotations goB ON ggmB.go_id = goB.go_id
        WHERE p.gene_a_id = ? AND p.gene_b_id = ?`

	rows, err := m.DB.Query(stmt, geneAId, geneBId)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var results []*models.FlatDBResult
	for rows.Next() {
		r := &models.FlatDBResult{}
		err := rows.Scan(
			&r.GeneASymbol, &r.GeneBSymbol, &r.PredictionScore, &r.Label,
			&r.GseSource, &r.GseData,
			&r.GeneAGoID, &r.GeneAGoDescription,
			&r.GeneBGoID, &r.GeneBGoDescription,
		)
		if err != nil {
			return nil, err
		}
		results = append(results, r)
	}

	if err = rows.Err(); err != nil {
		return nil, err
	}

	if len(results) == 0 {
		return nil, ErrNoRecord
	}

	return results, nil
}

// --- [新增函数] ---
// GetAllForGeneSymbol 查询与单个基因相关的所有记录，并包含它们的GO注释。
func (m *PredictionModel) GetAllForGeneSymbol(geneSymbol string) ([]*models.FlatDBResult, error) {
	var geneId int

	// 步骤1: 获取该基因的ID
	stmtId := `SELECT gene_id FROM genes WHERE symbol = ?`
	err := m.DB.QueryRow(stmtId, geneSymbol).Scan(&geneId)
	if err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return nil, ErrNoRecord
		}
		return nil, err
	}

	// 步骤2: 构建JOIN查询，查找所有包含该geneId的预测记录
	// WHERE子句会查找该ID出现在gene_a_id或gene_b_id列中的所有情况
	stmt := `
        SELECT
            gA.symbol AS gene_a_symbol, gB.symbol AS gene_b_symbol,
            p.prediction_score, p.label, p.gse_source, p.gse_data,
			p.binary_prediction, -- 为了内部排序逻辑，需要这个字段
            goA.go_id AS gene_a_go_id, goA.description AS gene_a_go_description,
            goB.go_id AS gene_b_go_id, goB.description AS gene_b_go_description
        FROM predictions p
        JOIN genes gA ON p.gene_a_id = gA.gene_id
        JOIN genes gB ON p.gene_b_id = gB.gene_id
        LEFT JOIN gene_go_mapping ggmA ON p.gene_a_id = ggmA.gene_id
        LEFT JOIN go_annotations goA ON ggmA.go_id = goA.go_id
        LEFT JOIN gene_go_mapping ggmB ON p.gene_b_id = ggmB.gene_id
        LEFT JOIN go_annotations goB ON ggmB.go_id = goB.go_id
        WHERE p.gene_a_id = ? OR p.gene_b_id = ?`

	rows, err := m.DB.Query(stmt, geneId, geneId)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	// 注意：这里的FlatDBResult结构需要临时能接收BinaryPrediction
	// 为了不修改models.go，我们可以在这里动态处理，但更规范的做法是修改模型
	// 为保持简洁，我们先假设FlatDBResult已经添加了BinaryPrediction字段
	var results []*models.FlatDBResult
	for rows.Next() {
		r := &models.FlatDBResult{}
		err := rows.Scan(
			&r.GeneASymbol, &r.GeneBSymbol, &r.PredictionScore, &r.Label,
			&r.GseSource, &r.GseData, &r.BinaryPrediction, // 接收binary_prediction
			&r.GeneAGoID, &r.GeneAGoDescription,
			&r.GeneBGoID, &r.GeneBGoDescription,
		)
		if err != nil {
			return nil, err
		}
		results = append(results, r)
	}

	if err = rows.Err(); err != nil {
		return nil, err
	}

	return results, nil
}
