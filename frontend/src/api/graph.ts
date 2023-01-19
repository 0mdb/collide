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

export async function getSampleGraph() {
  return axios.get<Graph[]>('/forcegraph/sample').then((res) => res.data)
}

// export async function getOptions({ }) {
//   return axios.get<SearchQuery[]>('/forcegraph/search_options', 'alex').then((res) => res.data)
// }

export async function getSearch() {
  return axios.post<SearchQuery[]>('/forcegraph/search').then((res) => res.data)
}

export const getOptions = (query: string) => {  
  return axios.post<SearchQuery[]>('/forcegraph/search_options?query', query).then((res) => res.data)
}
  // 'http://localhost/api/v1/forcegraph/search_options?query=alex'