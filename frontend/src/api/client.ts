// BidPilot API 客户端
import type { AnalysisResult, SampleTender, HealthResult } from '../types';

const API_BASE = '/api';

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const resp = await fetch(`${API_BASE}${url}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!resp.ok) {
    const text = await resp.text();
    throw new Error(`API Error ${resp.status}: ${text}`);
  }
  return resp.json();
}

export const api = {
  health: () => request<HealthResult>('/health'),

  listSampleTenders: () => request<SampleTender[]>('/sample-tenders'),

  analyzeTender: (tenderId: string) =>
    request<AnalysisResult>('/tenders/analyze', {
      method: 'POST',
      body: JSON.stringify({ tender_id: tenderId }),
    }),

  uploadTender: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const resp = await fetch(`${API_BASE}/tenders/upload`, {
      method: 'POST',
      body: formData,
    });
    if (!resp.ok) throw new Error('上传失败');
    return resp.json();
  },

  generateSolution: (taskId: string, tenderId: string = '') =>
    request('/bid/solution', {
      method: 'POST',
      body: JSON.stringify({ task_id: taskId, tender_id: tenderId }),
    }),

  generateResponseTable: (taskId: string, tenderId: string = '') =>
    request('/bid/response-table', {
      method: 'POST',
      body: JSON.stringify({ task_id: taskId, tender_id: tenderId }),
    }),

  complianceCheck: (taskId: string, tenderId: string = '') =>
    request('/bid/compliance-check', {
      method: 'POST',
      body: JSON.stringify({ task_id: taskId, tender_id: tenderId }),
    }),

  exportMarkdown: (taskId: string, reportType: string = 'all') =>
    request('/export/markdown', {
      method: 'POST',
      body: JSON.stringify({ task_id: taskId, report_type: reportType }),
    }),
};
