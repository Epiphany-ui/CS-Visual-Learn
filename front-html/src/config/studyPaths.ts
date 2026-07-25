/**
 * 公共学习路径配置
 * 供 StudyPath、CommunityFeed、Sandbox 等组件共用
 */
export interface StudyItem {
  name: string
  wikiSlug: string
  prompt: string
  difficulty: string
  estimatedMinutes: number
  prerequisites?: string[]
}

export interface Chapter {
  id: string; name: string; description: string; items: StudyItem[]
}

export interface StudyPath {
  id: string; name: string; desc: string; color: string; icon: string; chapters: Chapter[]
}

export const paths: StudyPath[] = [
  {
    id: 'ds', name: '数据结构入门', desc: '从线性表到高级树结构，逐个生成动画直观理解', color: '#7c3aed', icon: 'DataAnalysis',
    chapters: [
      { id: 'ch1', name: '线性表', description: '最基础的数据组织方式',
        items: [
          { name: '栈 (Stack)', wikiSlug: 'stack', prompt: '栈的 push 和 pop 操作动画演示，展示后进先出特性', difficulty: '入门', estimatedMinutes: 15 },
          { name: '队列 (Queue)', wikiSlug: 'queue', prompt: '队列的入队出队操作可视化动画', difficulty: '入门', estimatedMinutes: 15 },
          { name: '链表 (Linked List)', wikiSlug: 'linked-list', prompt: '链表插入删除节点的动画演示，展示指针操作', difficulty: '入门', estimatedMinutes: 20 },
          { name: '哈希表 (Hash Table)', wikiSlug: 'hash-table', prompt: '哈希表存储和冲突解决的可视化动画', difficulty: '中等', estimatedMinutes: 25, prerequisites: ['链表 (Linked List)'] },
        ],
      },
      { id: 'ch2', name: '树结构', description: '层次化数据模型',
        items: [
          { name: '二叉树 (Binary Tree)', wikiSlug: 'binary-tree', prompt: '二叉树三种遍历方式的可视化对比动画', difficulty: '中等', estimatedMinutes: 25, prerequisites: ['栈 (Stack)', '队列 (Queue)'] },
          { name: '二叉搜索树 (BST)', wikiSlug: 'binary-search-tree', prompt: '二叉搜索树插入查找删除操作的动画演示', difficulty: '中等', estimatedMinutes: 25, prerequisites: ['二叉树 (Binary Tree)'] },
          { name: '堆 (Heap)', wikiSlug: 'heap', prompt: '堆的建堆和调整过程动画，展示优先队列原理', difficulty: '中等', estimatedMinutes: 20, prerequisites: ['二叉树 (Binary Tree)'] },
        ],
      },
      { id: 'ch3', name: '高级树结构', description: '高效查找与存储',
        items: [
          { name: 'AVL 树', wikiSlug: 'avl-tree', prompt: 'AVL 树自平衡旋转操作的动画演示', difficulty: '困难', estimatedMinutes: 30, prerequisites: ['二叉搜索树 (BST)'] },
          { name: '线段树 (Segment Tree)', wikiSlug: 'segment-tree', prompt: '线段树构建和区间查询的可视化动画', difficulty: '困难', estimatedMinutes: 30, prerequisites: ['二叉树 (Binary Tree)'] },
          { name: '字典树 (Trie)', wikiSlug: 'trie', prompt: 'Trie 树插入和前缀搜索的动画演示', difficulty: '中等', estimatedMinutes: 20 },
        ],
      },
    ],
  },
  {
    id: 'algo', name: '算法基础', desc: '从排序到分治，掌握经典算法设计思想', color: '#f59e0b', icon: 'Operation',
    chapters: [
      { id: 'ch1', name: '查找与二分', description: '高效查找的基石',
        items: [
          { name: '二分查找', wikiSlug: 'binary-search', prompt: '二分查找算法的执行过程动画，展示分治思想', difficulty: '入门', estimatedMinutes: 15 },
          { name: '滑动窗口', wikiSlug: 'sliding-window', prompt: '滑动窗口算法解决子数组问题的动画演示', difficulty: '中等', estimatedMinutes: 20, prerequisites: ['二分查找'] },
          { name: '双指针', wikiSlug: 'two-pointers', prompt: '双指针技巧解决数组问题的可视化动画', difficulty: '中等', estimatedMinutes: 20 },
        ],
      },
      { id: 'ch2', name: '排序算法', description: '经典的排序策略对比',
        items: [
          { name: '冒泡排序', wikiSlug: 'bubble-sort', prompt: '冒泡排序算法执行过程可视化动画', difficulty: '入门', estimatedMinutes: 15 },
          { name: '归并排序', wikiSlug: 'merge-sort', prompt: '归并排序分治合并过程动画演示', difficulty: '中等', estimatedMinutes: 25 },
          { name: '快速排序', wikiSlug: 'quick-sort', prompt: '快速排序算法分治过程动画演示', difficulty: '中等', estimatedMinutes: 25, prerequisites: ['归并排序'] },
          { name: '堆排序', wikiSlug: 'heap-sort', prompt: '堆排序建堆和排序过程动画演示', difficulty: '中等', estimatedMinutes: 20, prerequisites: ['堆 (Heap)'] },
        ],
      },
      { id: 'ch3', name: '算法设计思想', description: '通用的问题求解策略',
        items: [
          { name: '贪心算法', wikiSlug: 'greedy', prompt: '贪心算法求解问题的动画演示', difficulty: '中等', estimatedMinutes: 25 },
          { name: '分治算法', wikiSlug: 'divide-and-conquer', prompt: '分治算法分解合并过程的可视化动画', difficulty: '中等', estimatedMinutes: 25 },
          { name: '回溯算法', wikiSlug: 'backtracking', prompt: '回溯算法搜索解空间的可视化动画', difficulty: '困难', estimatedMinutes: 30, prerequisites: ['分治算法'] },
        ],
      },
    ],
  },
  {
    id: 'graph', name: '图论基础', desc: '理解图的结构、遍历和最短路算法', color: '#06b6d4', icon: 'Connection',
    chapters: [
      { id: 'ch1', name: '图的遍历', description: '探索图的基础方法',
        items: [
          { name: '广度优先搜索 (BFS)', wikiSlug: 'bfs', prompt: 'BFS 逐层探索图的动画演示，展示最短路径性质', difficulty: '中等', estimatedMinutes: 25 },
          { name: '深度优先搜索 (DFS)', wikiSlug: 'dfs', prompt: 'DFS 递归探索图的动画演示', difficulty: '中等', estimatedMinutes: 25 },
          { name: '拓扑排序', wikiSlug: 'topological-sort', prompt: '拓扑排序的 Kahn 算法动画演示', difficulty: '中等', estimatedMinutes: 20, prerequisites: ['深度优先搜索 (DFS)'] },
        ],
      },
      { id: 'ch2', name: '最短路径', description: '找到最优路径',
        items: [
          { name: 'Dijkstra 算法', wikiSlug: 'dijkstra算法', prompt: 'Dijkstra 最短路径算法的动画演示', difficulty: '中等', estimatedMinutes: 30, prerequisites: ['广度优先搜索 (BFS)'] },
          { name: 'Bellman-Ford 算法', wikiSlug: 'bellman-ford算法', prompt: 'Bellman-Ford 算法处理负权边的动画演示', difficulty: '困难', estimatedMinutes: 30, prerequisites: ['Dijkstra 算法'] },
          { name: 'Floyd-Warshall 算法', wikiSlug: 'floyd-warshall算法', prompt: 'Floyd-Warshall 全源最短路径动画演示', difficulty: '困难', estimatedMinutes: 25, prerequisites: ['Dijkstra 算法'] },
        ],
      },
      { id: 'ch3', name: '图的高级主题', description: '更深入的图论应用',
        items: [
          { name: '最小生成树', wikiSlug: 'minimum-spanning-tree', prompt: 'Prim/Kruskal 最小生成树算法动画', difficulty: '中等', estimatedMinutes: 25, prerequisites: ['Dijkstra 算法'] },
          { name: '网络流', wikiSlug: 'network-flow', prompt: '最大流 Ford-Fulkerson 算法动画演示', difficulty: '困难', estimatedMinutes: 35, prerequisites: ['广度优先搜索 (BFS)'] },
          { name: '最短路径总览', wikiSlug: 'shortest-path', prompt: '多种最短路径算法对比可视化动画', difficulty: '中等', estimatedMinutes: 20, prerequisites: ['Dijkstra 算法'] },
        ],
      },
    ],
  },
  {
    id: 'dp', name: '动态规划', desc: '掌握状态转移的思维方式', color: '#10b981', icon: 'Histogram',
    chapters: [
      { id: 'ch1', name: '基础概念', description: '理解 DP 的核心思想',
        items: [
          { name: '动态规划入门', wikiSlug: 'dynamic-programming', prompt: '动态规划核心思想：状态转移的可视化动画', difficulty: '中等', estimatedMinutes: 30 },
          { name: '编辑距离', wikiSlug: 'edit-distance', prompt: '编辑距离 DP 填表过程动画演示', difficulty: '中等', estimatedMinutes: 25, prerequisites: ['动态规划入门'] },
        ],
      },
      { id: 'ch2', name: '经典问题', description: 'DP 的经典应用场景',
        items: [
          { name: '背包问题', wikiSlug: 'knapsack', prompt: '0-1 背包问题 DP 求解过程动画演示', difficulty: '中等', estimatedMinutes: 25, prerequisites: ['动态规划入门'] },
          { name: '最长公共子序列 (LCS)', wikiSlug: 'lcs', prompt: 'LCS 动态规划填表回溯过程动画', difficulty: '中等', estimatedMinutes: 25, prerequisites: ['动态规划入门'] },
          { name: '最长递增子序列 (LIS)', wikiSlug: 'lis', prompt: 'LIS 动态规划求解过程可视化动画', difficulty: '中等', estimatedMinutes: 20, prerequisites: ['最长公共子序列 (LCS)'] },
        ],
      },
      { id: 'ch3', name: '进阶技巧', description: '高级 DP 技术',
        items: [
          { name: '状态压缩 DP', wikiSlug: '状态压缩动态规划', prompt: '状态压缩动态规划的位运算技巧动画', difficulty: '困难', estimatedMinutes: 35, prerequisites: ['背包问题'] },
        ],
      },
    ],
  },
  {
    id: 'math', name: '高等数学', desc: '用动画理解极限、微积分的几何意义', color: '#3b82f6', icon: 'TrendCharts',
    chapters: [
      { id: 'ch1', name: '极限与连续', description: '微积分的基石',
        items: [
          { name: '极限 (Limit)', wikiSlug: 'limit', prompt: '函数趋近于某点时极限的可视化动画', difficulty: '中等', estimatedMinutes: 20 },
          { name: '级数 (Series)', wikiSlug: 'series', prompt: '数列级数收敛发散的动画演示', difficulty: '中等', estimatedMinutes: 25, prerequisites: ['极限 (Limit)'] },
        ],
      },
      { id: 'ch2', name: '微分学', description: '变化率与优化',
        items: [
          { name: '导数', wikiSlug: 'derivative', prompt: '导数的切线斜率几何意义动画演示', difficulty: '中等', estimatedMinutes: 25, prerequisites: ['极限 (Limit)'] },
          { name: '偏导数', wikiSlug: 'partial-derivative', prompt: '多元函数偏导数的几何解释动画', difficulty: '中等', estimatedMinutes: 20, prerequisites: ['导数'] },
          { name: '泰勒级数', wikiSlug: 'taylor-series', prompt: '泰勒级数多项式逼近函数的动画', difficulty: '中等', estimatedMinutes: 25, prerequisites: ['导数'] },
          { name: '梯度下降', wikiSlug: 'gradient-descent', prompt: '梯度下降法寻找最小值的迭代过程动画', difficulty: '中等', estimatedMinutes: 25, prerequisites: ['偏导数'] },
        ],
      },
      { id: 'ch3', name: '积分学与进阶', description: '面积、体积与变换',
        items: [
          { name: '定积分', wikiSlug: 'integral', prompt: '定积分黎曼和逼近过程动画', difficulty: '中等', estimatedMinutes: 25, prerequisites: ['极限 (Limit)'] },
          { name: '傅里叶级数', wikiSlug: 'fourier-series', prompt: '傅里叶级数逼近方波的可视化动画', difficulty: '中等', estimatedMinutes: 30, prerequisites: ['泰勒级数'] },
        ],
      },
    ],
  },
  {
    id: 'algebra', name: '线性代数', desc: '矩阵变换、特征值的几何直观理解', color: '#8b5cf6', icon: 'Grid',
    chapters: [
      { id: 'ch1', name: '矩阵与变换', description: '线性代数的基本对象',
        items: [
          { name: '矩阵运算', wikiSlug: 'matrix', prompt: '矩阵乘法行列对应计算过程动画', difficulty: '入门', estimatedMinutes: 20 },
          { name: '行列式', wikiSlug: 'determinant', prompt: '行列式的几何意义：面积/体积变换动画', difficulty: '中等', estimatedMinutes: 25, prerequisites: ['矩阵运算'] },
        ],
      },
      { id: 'ch2', name: '线性变换', description: '空间变换的几何直观',
        items: [
          { name: '线性变换', wikiSlug: 'linear-transformation', prompt: '线性变换对空间形变影响的可视化动画', difficulty: '中等', estimatedMinutes: 25, prerequisites: ['矩阵运算'] },
          { name: '向量空间', wikiSlug: 'vector-space', prompt: '向量空间基变换的动画演示', difficulty: '中等', estimatedMinutes: 25 },
          { name: '正交基', wikiSlug: 'orthogonal-basis', prompt: 'Gram-Schmidt 正交化过程动画', difficulty: '中等', estimatedMinutes: 25, prerequisites: ['向量空间'] },
        ],
      },
      { id: 'ch3', name: '特征分解', description: '矩阵的核心不变量',
        items: [
          { name: '特征值与特征向量', wikiSlug: 'eigenvalue', prompt: '特征向量和特征值的几何直观动画', difficulty: '中等', estimatedMinutes: 30, prerequisites: ['线性变换'] },
          { name: '矩阵对角化', wikiSlug: 'diagonalization', prompt: '矩阵对角化分解过程可视化', difficulty: '困难', estimatedMinutes: 30, prerequisites: ['特征值与特征向量'] },
        ],
      },
    ],
  },
  {
    id: 'prob', name: '概率统计', desc: '从随机变量到统计推断', color: '#ec4899', icon: 'PieChart',
    chapters: [
      { id: 'ch1', name: '概率基础', description: '理解随机性',
        items: [
          { name: '概率论基础', wikiSlug: 'probability-theory', prompt: '概率基本概念和公理的可视化动画', difficulty: '入门', estimatedMinutes: 20 },
          { name: '贝叶斯定理', wikiSlug: 'bayes-theorem', prompt: '贝叶斯定理条件概率更新的动画演示', difficulty: '中等', estimatedMinutes: 25, prerequisites: ['概率论基础'] },
        ],
      },
      { id: 'ch2', name: '概率分布', description: '描述随机变量的行为',
        items: [
          { name: '正态分布', wikiSlug: 'normal-distribution', prompt: '正态分布的概率密度函数和性质动画', difficulty: '中等', estimatedMinutes: 20, prerequisites: ['概率论基础'] },
          { name: '中心极限定理', wikiSlug: 'central-limit-theorem', prompt: '中心极限定理的采样分布收敛动画', difficulty: '中等', estimatedMinutes: 25, prerequisites: ['正态分布'] },
          { name: '大数定律', wikiSlug: 'law-of-large-numbers', prompt: '大数定律样本均值收敛过程动画', difficulty: '中等', estimatedMinutes: 20, prerequisites: ['概率论基础'] },
        ],
      },
      { id: 'ch3', name: '随机过程', description: '随时间演化的随机系统',
        items: [
          { name: '马尔可夫链', wikiSlug: 'markov-chain', prompt: '马尔可夫链状态转移的可视化动画', difficulty: '困难', estimatedMinutes: 30, prerequisites: ['概率论基础'] },
        ],
      },
    ],
  },
]

/** 根据路径 ID 查找学习路径 */
export function getStudyPathById(id: string): StudyPath | undefined {
  return paths.find(p => p.id === id)
}

/** 根据知识点 wikiSlug 查找知识点名称 */
export function getKnowledgeNameBySlug(slug: string): string | undefined {
  for (const p of paths) {
    for (const ch of p.chapters) {
      const item = ch.items.find(i => i.wikiSlug === slug)
      if (item) return item.name
    }
  }
  return undefined
}
