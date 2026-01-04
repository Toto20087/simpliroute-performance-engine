import axios from 'axios';

// Use environment variable or default to localhost
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export interface Stop {
    lat: number;
    lng: number;
    address: string;
}

export interface OptimizationRequest {
    stops: Stop[];
    depot?: Stop;
}

export interface OptimizationResponse {
    route_id: string;
    optimized_order: string[]; // List of addresses
    total_distance_km: number;
    estimated_travel_time_minutes: number;
    execution_time_seconds: number;
    status: string;
}

export interface TaskResponse {
    task_id: string;
    status: string;
}

export interface TaskResult {
    task_id: string;
    status: string;
    result?: OptimizationResponse;
}

export const api = {
    optimize: async (data: OptimizationRequest): Promise<TaskResponse> => {
        const response = await axios.post(`${API_BASE_URL}/optimize`, data);
        return response.data;
    },

    getTaskStatus: async (taskId: string): Promise<TaskResult> => {
        const response = await axios.get(`${API_BASE_URL}/tasks/${taskId}`);
        return response.data;
    }
};
