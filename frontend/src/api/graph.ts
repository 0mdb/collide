import axios from './axios'

interface Graph {
    nodes: any[],
    links: any[],
}

export function getGraph() {
  return axios.get<Graph[]>('/forcegraph/sample').then(res => res.data)
}


