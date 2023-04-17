import { API_URL } from "./api_constants"

export class YearlyAggregate {
  year!: number
  count!: number
}

export class ProjectAggregate {
  pcode!: string
  count!: number
  title!: string
  year!: number
}

export class Stats {
  projectStats!: YearlyAggregate[]
  submissionStats!: YearlyAggregate[]
  awardStats!: YearlyAggregate[]
  projectAwardStats!: ProjectAggregate[]
}

export async function getStats(id: string): Promise<Stats> {
  return await (await fetch(`${API_URL}/stats/${id}`)).json()
}
