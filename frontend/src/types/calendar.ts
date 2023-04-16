export class TimeRange {
  start!: string
  end!: string
}

export class Event {
  id!: number
  url!: string
  title!: string
  time!: TimeRange
  description!: string
  tags!: string
  conference!: boolean
  competition!: boolean
}
