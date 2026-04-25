# collide

A force-graph + Sankey visualization tool for Canadian government lobbying activity. Built originally for **[lobbyradar.io](https://lobbyradar.io)** to let journalists, researchers, and civic-tech folks explore who's lobbying whom, on which bills, with what money.

> **Status: dormant.** Active development ended in March 2023. The repo is published as-is for anyone interested in the approach or in resurrecting it. Production deployment requires merging the feature branches back to `main` (see [branch state](#branch-state) below).

## What it shows

The deployed site rendered an interactive force-directed graph of **persons**, **organizations**, and the relationships between them, plus a Sankey diagram for following flows of funding and influence.

Three relationship types drove the graph:

| Edge type | Meaning | Style |
|---|---|---|
| `MEMBERSHIP` | Person belongs to an organization (e.g. lobbyist→firm, MP→party, director→corp) | Solid black |
| `COMMUNICATION` | Recorded lobbying contact between two people (e.g. lobbyist→DPoH) | Dashed red |
| `FUNDING` | Money flow between organizations (donations, grants, sponsorships) | Dashed green |

Search any person, organization, or sector and the graph centred on that node, with neighbours expanded out to a configurable depth. Hovering a node highlighted everything they touched.

## Data sources

| Source | What it provides |
|---|---|
| Parliament of Canada (XML scrape) | Sitting MPs, cabinet members, committees |
| Canada Business Register | Federal corporate numbers, directors |
| TSX board listings | Public-company board memberships |
| Alberta lobbyist registry | Lobbyists, principals, communications, contracts (Alberta scope) |

Ingestion ran ad-hoc — there's no live cron pipeline in the codebase. Snapshots were imported into Postgres + Memgraph as one-off batches.

## Architecture

```
┌──────────────┐    HTTP    ┌──────────────────────┐    Cypher    ┌──────────┐
│   Browser    │  ────────► │  FastAPI (Python)    │  ──────────► │ Memgraph │
│  React + TS  │  ◄──────── │  + NetworkX shaper   │              └──────────┘
│  react-force-│            │  + Celery workers    │              ┌──────────┐
│  graph,      │            │  + FastAPI-Users JWT │  ──SQL────► │ Postgres │
│  ECharts     │            └──────────────────────┘              └──────────┘
└──────────────┘                                                        ▲
                                                                  scrapers
                                                              (XML / CSV one-shot)
```

**Backend:** FastAPI, SQLAlchemy, Celery + Redis, NetworkX for graph shaping, [Memgraph](https://memgraph.com/) for the graph store, Postgres for everything else, FastAPI-Users for JWT auth.

**Frontend:** React 18 + TypeScript + Vite, [react-force-graph](https://github.com/vasturiano/react-force-graph) (2D), [ECharts](https://echarts.apache.org/) Sankey, Tailwind + [Blueprint.js](https://blueprintjs.com/), TanStack Query, react-router-dom v6.

**Infra:** Docker Compose, Traefik v2 reverse proxy, PgAdmin for DB inspection.

## Branch state

The codebase fragmented across feature branches that were never merged back. To get the deployed site running, you need pieces from at least three branches:

| Branch | What's in it |
|---|---|
| `main` | Cookiecutter scaffolding, auth backend, Docker compose. **No graph endpoints.** Currently has a Vue 2 frontend leftover. |
| `frontend-react-demo` | The deployed React 18 frontend with the working force graph + Sankey UI |
| `6-main-graph-profile-memgraph-queryaggregation-script-and-optimize` | The Memgraph query aggregation, NetworkX shaper, and `/api/v1/c/forcegraph/*` endpoints |
| `deploy-ec2` | EC2 / Docker Swarm deployment glue |

A reasonable starting point if you're reviving this: branch off `frontend-react-demo`, cherry-pick the graph endpoints from `6-main-graph-...`, then bring dependencies up to current versions.

## Quick start (development, scaffolding only)

```bash
git clone https://github.com/0mdb/collide.git
cd collide
cp .env.example .env
cp frontend/.env.example frontend/.env
# Edit .env values — at minimum SECRET_KEY, POSTGRES_PASSWORD, FIRST_SUPERUSER_PASSWORD
docker compose up -d
```

Once up:
- Backend (Swagger): http://localhost/api/v1/docs
- Frontend: http://localhost
- PgAdmin: http://localhost:5050
- Traefik dashboard: http://localhost:8090

This runs the `main`-branch scaffolding only — the graph UI is not on this branch (see above).

## Configuration

All runtime config goes through `.env` (root) and `frontend/.env`. Both have `.env.example` templates committed; **never commit the populated `.env` files**, they're git-ignored. If you're connecting a real SES / SMTP provider, generate the credentials fresh — the credentials previously committed to this repo are revoked.

## License

No license file. The code is published for reference; if you want to fork and use it, open an issue and we'll sort licensing out.

## Acknowledgements

Bootstrapped from [`tiangolo/full-stack-fastapi-postgresql`](https://github.com/tiangolo/full-stack-fastapi-postgresql). Force-graph rendering via [vasturiano/react-force-graph](https://github.com/vasturiano/react-force-graph). Graph storage via [Memgraph](https://memgraph.com/).
