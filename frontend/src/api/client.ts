// BidPilot API 客户端
import type { AnalysisResult, SampleTender, HealthResult } from '../types';
import { getMockAnalysisResult, getMockUploadResult, mockHealth, mockSampleTenders } from './mockData';

const API_BASE = import.meta.env.VITE_API_BASE_URL || (import.meta.env.DEV ? '/api' : '');
const USE_STATIC_MOCK = API_BASE === '';

function mockRequest<T>(url: string, options?: RequestInit): T | null {
  if (url === '/health') return mockHealth as T;
  if (url === '/sample-tenders') return mockSampleTenders as T;

  if (url === '/tenders/analyze' && options?.body) {
    const body = JSON.parse(String(options.body)) as { tender_id?: string };
    return getMockAnalysisResult(body.tender_id || 'sample_001') as T;
  }

  if (url === '/export/markdown') {
    return { status: 'ok', files: [] } as T;
  }

  return null;
}

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  if (USE_STATIC_MOCK) {
    const fallback = mockRequest<T>(url, options);
    if (fallback) return fallback;
  }

  try {
    const resp = await fetch(`${API_BASE}${url}`, {
      headers: { 'Content-Type': 'application/json' },
      ...options,
    });
    if (!resp.ok) {
      const fallback = mockRequest<T>(url, options);
      if (fallback && (resp.status === 404 || resp.status === 405)) return fallback;
      const text = await resp.text();
      throw new Error(`API Error ${resp.status}: ${text}`);
    }
    return resp.json();
  } catch (error) {
    const fallback = mockRequest<T>(url, options);
    if (fallback) return fallback;
    throw error;
  }
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
    if (USE_STATIC_MOCK) return getMockUploadResult(file.name);

    const formData = new FormData();
    formData.append('file', file);
    try {
      const resp = await fetch(`${API_BASE}/tenders/upload`, {
        method: 'POST',
        body: formData,
      });
      if (!resp.ok) {
        if (resp.status === 404 || resp.status === 405) return getMockUploadResult(file.name);
        throw new Error('上传失败');
      }
      return resp.json();
    } catch {
      return getMockUploadResult(file.name);
    }
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
