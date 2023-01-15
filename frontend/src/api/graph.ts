import axios from './axios'

interface Graph {
    nodes: {
      "id": string,
      "name": string,
      "person": boolean,
      "db_id": string,
    },
    links: any[],
}

export function getGraph() {
  return axios.get<Graph[]>('/forcegraph/sample').then(res => res.data)
}


