// file: pkg/models/mysql/predictions.go
package mysql

import (
	"database/sql"
	"errors" // 用于处理特定的数据库错误

	"geneprediction.wozonet.net/pkg/models" // 导入我们定义的模型
)

// 定义一个自定义错误，当查询不到记录时返回，便于上层处理。
var ErrNoRecord = errors.New("models: no matching record found")

// PredictionModel 封装了数据库连接池。
type PredictionModel struct {
	DB *sql.DB
}

// GetOne 查询单个基因对的预测记录。
func (m *PredictionModel) GetOne(geneA, geneB string) (*models.Prediction, error) {
	// 我们的Python脚本逻辑是A,B都可以查，但数据库里是标准化的
	// 为了简化，我们假设查询时也会尝试标准化查询
	// 如果gene_predictions表不是标准化的，这里的逻辑需要调整
	stmt := `SELECT GeneA, GeneB, Prediction, label AS PredictingRelation, BinaryPrediction, label
             FROM gene_predictions WHERE (GeneA = ? AND GeneB = ?) OR (GeneA = ? AND GeneB = ?)`

	row := m.DB.QueryRow(stmt, geneA, geneB, geneB, geneA)

	p := &models.Prediction{}

	err := row.Scan(&p.GeneA, &p.GeneB, &p.PredictionScore, &p.PredictingRelation, &p.BinaryPrediction, &p.Label)
	if err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return nil, ErrNoRecord
		}
		return nil, err
	}
	return p, nil
}

// GetAllForGeneA 查询与单个基因相关的所有记录。
func (m *PredictionModel) GetAllForGeneA(geneA string) ([]*models.Prediction, error) {
	stmt := `SELECT GeneA, GeneB, Prediction, label AS PredictingRelation, BinaryPrediction, label
             FROM gene_predictions WHERE GeneA = ? OR GeneB = ?`

	rows, err := m.DB.Query(stmt, geneA, geneA)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	predictions := []*models.Prediction{}
	for rows.Next() {
		p := &models.Prediction{}
		err := rows.Scan(&p.GeneA, &p.GeneB, &p.PredictionScore, &p.PredictingRelation, &p.BinaryPrediction, &p.Label)
		if err != nil {
			return nil, err
		}
		predictions = append(predictions, p)
	}

	if err = rows.Err(); err != nil {
		return nil, err
	}

	return predictions, nil
}
