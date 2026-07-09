import { pythonClient } from './client'
import type { ApiResponse } from '@/types/api'
import type { VideoFile, VideoMetadata, FrameInfo } from '@/types/task'

const VIDEO_BASE = 'http://localhost:8000'

export const videosApi = {
  /** 获取视频列表 */
  getList() {
    return pythonClient.get<ApiResponse<{ items: VideoFile[]; total: number }>>('/api/videos/list')
  },

  /** 下载视频 */
  getDownloadUrl(filename: string): string {
    return `${VIDEO_BASE}/api/videos/${filename}/download`
  },

  /** 视频播放 URL */
  getPlayUrl(filename: string): string {
    return `${VIDEO_BASE}/videos/${filename}`
  },

  /** 转换为 GIF */
  convertGif(filename: string, fps = 10, width = 480) {
    return pythonClient.post<ApiResponse<{ filename: string; url: string; size_kb: number }>>(`/api/videos/${filename}/convert/gif`, null, {
      params: { fps, width },
    })
  },

  /** 删除视频 */
  deleteVideo(filename: string) {
    return pythonClient.delete(`/api/videos/${filename}`)
  },
}

export const debugApi = {
  /** 获取视频元数据 */
  getVideoInfo(filename: string) {
    return pythonClient.get<ApiResponse<VideoMetadata>>(`/api/debug/video/${filename}/info`)
  },

  /** 提取帧 */
  extractFrames(filename: string, startFrame = 0, endFrame = 10) {
    return pythonClient.get<ApiResponse<{ frames: FrameInfo[]; total_extracted: number }>>(`/api/debug/video/${filename}/frames`, {
      params: { start_frame: startFrame, end_frame: endFrame, format: 'jpg', quality: 85 },
    })
  },

  /** 获取缩略图网格 */
  getThumbnailSheet(filename: string, cols = 5, rows = 4) {
    return pythonClient.get<ApiResponse<{ url: string; cols: number; rows: number }>>(`/api/debug/video/${filename}/thumbnail-sheet`, {
      params: { cols, rows },
    })
  },
}
