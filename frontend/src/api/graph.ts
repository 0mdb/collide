import axios from './axios'

interface Graph {
  nodes: {
    id: string
    name: string
    type: string
    val: number
  }
  links: {
    source: 'string'
    target: 'string'
    type: 'string'
    color: 'string'
    dash: [0]
    amount: 0
  }
}

interface SearchQuery {
  query: string
}

export async function getGraph() {
  return axios.get<Graph[]>('/forcegraph/sample').then((res) => res.data)
}

export async function getOptions() {
  return axios.get<SearchQuery[]>('/forcegraph/search_options').then((res) => res.data)
}

export async function getSearch() {
  return axios.get<SearchQuery[]>('/forcegraph/search').then((res) => res.data)
}
