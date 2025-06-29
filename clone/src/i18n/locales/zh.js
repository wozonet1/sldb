export default {
  header: {
    home: '首页',
    search: '搜索',
    about: '关于',
    language: '语言'
  },
  home: {
    welcome: '欢迎使用 Struct2SL',
    subtitle: '发现合成致死基因对并深入了解基因相互作用。',
    searchPlaceholder: '搜索基因对...(例如: TSPAN1)',
    stats: {
      genePairs: '基因对',
      experiments: '实验',
      cancerTypes: '癌症类型',
      publications: '出版物'
    },
    updates: {
      title: '最近更新',
      newBreastCancer: {
        title: '新增乳腺癌相关基因对',
        content: '我们新增了342个与乳腺癌相关的合成致死基因对，为乳腺癌治疗提供了新的潜在靶点。',
        date: '更新于 2025-06-15'
      },
      websiteOptimization: {
        title: '网站界面优化',
        content: '我们对网站进行了界面优化，提升了用户体验和搜索功能，使数据检索更加便捷。',
        date: '更新于 2025-06-01'
      }
    },
    statistics: {
      title: 'Struct2SL 统计数据',
      description: 'Struct2SL使用来自SynLethDB的最新研究数据（人类合成致死基因对和非合成致死基因对）来预测潜在的基因对。当前版本覆盖了15794个人类基因，所呈现的结果是计算预测结果。',
      table: {
        header: {
          dataType: '数据类型',
          entityCount: '实体数量'
        },
        rows: {
          syntheticLethalPairs: '合成致死基因对',
          nonsyntheticLethalPairs: '非合成致死基因对',
          proteinSequence: '蛋白质序列',
          ppiNodesCount: '蛋白质-蛋白质相互作用网络（节点）',
          ppiEdgesCount: '蛋白质-蛋白质相互作用网络（边）',
          proteinStructure: '蛋白质空间结构'
        }
      }
    }
  },
  search: {
    title: '搜索基因对',
    gene1: '基因 1',
    gene2: '基因 2(可选)',
    inputPlaceholder: '输入基因名称(如TSPAN1)',
    searchButton: '搜索',
    results: '搜索结果',
    table: {
      gene1: '基因 1',
      gene2: '基因 2',
      predictionScore: '预测分数',
      predictingRelation: '预测关系',
      source: '来源'
    },
    pagination: {
      showing: '显示第',
      to: '到',
      of: '条，共',
      results: '条结果',
      previous: '上一页',
      next: '下一页',
      goToPage: '跳转到第',
      Page: '页',
      go: '跳转',
    },
    noResults: {
      title: '未找到匹配结果',
      suggestion: '尝试使用不同的搜索条件或关键词',
      reset: '重置搜索'
    },
    loading: '正在搜索...'
  },
  about: {
    title: '关于 Struct2SL',
    description: 'Struct2SL是一个专注于合成致死基因对的数据库，为癌症治疗提供潜在靶点。若想要了解更多信息,请点击',
    link: '这里',
    team:{
        mem1:{
          name: '王轩',
          role: '指导创业计划执行',
          description: "指导创业计划执行<br>\
                        哈工大（深圳）教授<br>\
                        哈深资产公司董事长<br>\
                      哈工大决策智能研究所所长<br>\
                    哈工大（深圳）计算机应用研究中心主任<br>\
                    广东省人工智能与机器人学会监事长等"
        },
        mem2:{
          name: '李君一',
          role: '指导合成致死算法开发',
          description: "哈工大（深圳）教授<br>\
                        博士生导师<br>\
                        发表60多篇国际期刊和会议文章<br>\
                        国家重点研发计划项目课题负责人<br>\
                        国家自然科学基金面上项目主持人"
        },
    },
    sections: {
      whatIs: {
        title: '什么是合成致死？',
        content: '合成致死是指两个基因之间的一种关系，当单独敲除其中一个基因时细胞仍然存活，但同时敲除两个基因时会导致细胞死亡。这一概念在癌症治疗中具有重要意义，因为它可以帮助我们找到针对癌细胞的特异性治疗靶点。'
      },
      ourMission: {
        title: '我们的使命',
        content: '我们致力于通过整合多种数据源和先进的计算方法，预测和验证合成致死基因对，为癌症精准治疗提供科学依据。'
      },
      
      
      contact: {
        title: '联系我们',
        email: '邮箱',
        phone: '电话'
      }
    }
  }
  ,
  footer: {
    about: {
      title: '关于 Struct2SL',
      description: 'Struct2SL是一个专注于合成致死基因对的数据库，为癌症治疗提供潜在靶点。'
    },
    quickLinks: {
      title: '快速链接',
      home: '首页',
      search: '搜索',
      about: '关于'
    },
    resources: {
      title: '资源',
      apiDocs: 'API文档',
      tutorials: '使用教程',
      download: '下载数据',
      faq: '常见问题'
    },
    contact: {
      title: '联系我们'
    },
    copyright: '保留所有权利。'
  }
}