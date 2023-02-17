import axios from './axios'

export interface graphDataType {
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
  return await axios.get<graphDataType>('/forcegraph/sample').then((res) => res.data)
}

export async function getGraph(query: string) {
  console.log('getGraph', query)
  return await axios.post('forcegraph/search/' + query).then((res) => res.data)
}

export async function getSearchResults(query: string) {
  const SEARCH_URL = 'forcegraph/search_options?query='
  const match_name = query.toLowerCase().split(' ').join('')
  console.log('getSearchResults', query)
  return await axios.post(SEARCH_URL + match_name).then((res) => res.data)
}
