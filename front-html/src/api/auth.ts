import { javaClient } from './client'
import type { ApiResponse, UserInfo } from '@/types/api'

export const authApi = {
  /** 注册 */
  register(username: string, password: string) {
    return javaClient.post<ApiResponse<UserInfo>>('/api/register', null, {
      params: { username, password },
    })
  },

  /** 登录 */
  login(username: string, password: string) {
    return javaClient.post<ApiResponse<UserInfo>>('/api/login', null, {
      params: { username, password },
    })
  },

  /** 提交生成任务 */
  submitTask(userInput: string, maxRetry = 3) {
    return javaClient.post<ApiResponse<number>>('/api/submit', null, {
      params: { userInput, maxRetry },
    })
  },

  /** 查询任务状态 */
  getTaskStatus(taskId: number) {
    return javaClient.get(`/api/task/status/${taskId}`)
  },

  /** 获取任务历史 */
  getTaskList() {
    return javaClient.get('/api/task/list')
  },
}
