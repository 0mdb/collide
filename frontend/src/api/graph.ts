import axios from './axios'

export interface graphDataType {
  nodes: {
    id: string
    name: string
    type: string
    value: number
    nodeColor: string
  }
  links: {
    source: string
    target: string
    type: string
    linkColor: string
    linkDirectionalArrowLength: 0
    linkDirectionalArrowRelPos: 0
    linkWidth: 1
    color: 'string'
    dash: [0]
    amount: 0
  }

}

interface SearchQuery {
  query: string
}

export async function getSampleGraph() {
  return await axios.get<graphDataType>('c/forcegraph/sample').then((res) => res.data)
}

export async function getGraph(query: string) {
  query = query.join('&')
  //console.log('getGraph', query)
  return await axios.post<graphDataType>('c/forcegraph/search/' + query).then((res) => res.data)
}

export async function getSearchResults(query: string) {
  const SEARCH_URL = 'c/forcegraph/search_options?query='
  const match_name = query.toLowerCase().split(' ').join('')
  //console.log('getSearchResults', query)
  //console.log(await axios.post<SearchQuery>(SEARCH_URL + match_name).then((res) => res.data))
  return await axios.post<SearchQuery>(SEARCH_URL + match_name).then((res) => res.data)
}
