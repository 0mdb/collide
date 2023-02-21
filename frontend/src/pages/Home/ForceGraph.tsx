import React, { useRef, useState, useLayoutEffect, useCallback } from 'react'
import { ForceGraph2D } from 'react-force-graph'
import { useQuery } from '@tanstack/react-query'
import Loading from '../../components/Loading'
import { useWindowSize } from '@react-hook/window-size'
import { getGraph } from '../../api/graph'
import useDarkMode from '../../hooks/useDarkMode'

function ForceGraph(props) {
  const [width, height] = useWindowSize()
  const fgRef = useRef(null)
  const [highlightNodes, setHighlightNodes] = useState(new Set())
  const [highlightLinks, setHighlightLinks] = useState(new Set())
  const [hoverNode, setHoverNode] = useState(null)

  const {
    data: graphData,
    status: graphStatus,
    isFetching,
  } = useQuery({
    queryKey: ['getGraph', props.selected],
    queryFn: () => getGraph(props.selected),
    enabled: !!props.selected,
    refetchOnWindowFocus: false,
  })

  useLayoutEffect(() => {
    if (graphStatus === 'success' && graphData) {
      // Make sure all nodes have the `neighbors` property
      graphData.nodes.forEach((node) => {
        node.neighbors = []
        node.links = []
      })

      // Populate the `neighbors` and `links` properties
      graphData.links.forEach((link) => {
        const { source, target } = link
        const sourceNode = graphData.nodes.find((node) => node.id === source)
        const targetNode = graphData.nodes.find((node) => node.id === target)

        if (sourceNode && targetNode) {
          sourceNode.neighbors.push(targetNode)
          targetNode.neighbors.push(sourceNode)

          sourceNode.links.push(link)
          targetNode.links.push(link)
        }
      })

      // Highlight the selected node
      const selectedNode = graphData.nodes.find((node) => node.id === props.selected)
      if (selectedNode) {
        highlightNodes.add(selectedNode)
        selectedNode.neighbors.forEach((neighbor) => highlightNodes.add(neighbor))
        selectedNode.links.forEach((link) => highlightLinks.add(link))
      }
    }
  }, [graphData, graphStatus, highlightNodes, highlightLinks, props.selected])

  const updateHighlight = useCallback(() => {
    setHighlightNodes(highlightNodes)
    setHighlightLinks(highlightLinks)
  }, [highlightNodes, highlightLinks])

  const handleNodeHover = useCallback(
    (node) => {
      highlightNodes.clear()
      highlightLinks.clear()
      if (node) {
        highlightNodes.add(node)
        node.neighbors.forEach((neighbor) => highlightNodes.add(neighbor))
        node.links.forEach((link) => highlightLinks.add(link))
      }
      setHoverNode(node || null)
    },
    [highlightNodes, highlightLinks],
  )

  const nodeCanvasObject = useCallback(
    (node, ctx, globalScale) => {
      const { x, y, id, label } = node
      const nodeRadius = 16
      const fontSize = id === props.selected ? 20 : 16
      const fontColor = props.darkMode ? '#fff' : '#000'
      // Draw outer ring
      ctx.beginPath()
      ctx.arc(x, y, nodeRadius, 0, 2 * Math.PI, false)
      ctx.lineWidth = 8 / globalScale
      ctx.strokeStyle = id === props.selected ? '#4338ca' : '#ffa31a'
      ctx.stroke()

      // Draw inner ring and label
      if (highlightNodes.has(node) || id === props.selected) {
        ctx.beginPath()
        ctx.arc(x, y, nodeRadius * 0.5, 0, 2 * Math.PI, false)

        ctx.fill()

        // Set canvas size to 100% of parent div

        // Draw label
        ctx.font = `${fontSize / globalScale}px sans`
        ctx.textAlign = 'center'
        ctx.fillStyle = fontColor
        //ctx.fillStyle = '#000000'
        ctx.fillText(node.name, x, y + nodeRadius + 12)
      }
    },
    [highlightNodes, props.selected],
  )

  const handleOnEngineStop = useCallback(
    (node, ctx) => {
      fgRef.current.zoomToFit(400)

      updateHighlight()
      //update font color
    },
    [updateHighlight],
  )

  return (
    <div className='m-0 flex h-full w-full flex-row items-center justify-center overflow-clip'>
      {isFetching ? (
        <Loading />
      ) : (
        <ForceGraph2D
          ref={fgRef}
          graphData={graphData}
          height={height}
          width={width}
          cooldownTicks={100}
          nodeAutoColorBy='id'
          linkDirectionalParticles='value'
          linkCurvature='curvature'
          //onEngineStop={() => fgRef.current.zoomToFit(200)}
          onEngineStop={handleOnEngineStop}
          onNodeClick={(node) => {
            console.log('node', node)
            props.setSelected(node.id)
          }}
          nodeCanvasObjectMode={(node) => (highlightNodes.has(node) ? 'before' : undefined)}
          nodeCanvasObject={nodeCanvasObject}
          //onNodeHover={handleNodeHover}
          //onLinkHover={handleLinkHover}
          /* style={{ height: '100%' }} */
        />
      )}
    </div>
  )
}

export default ForceGraph
