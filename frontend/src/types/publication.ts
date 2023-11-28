import { Institute } from "./admin";

export class Publication {
  title!: string;
  url!: string;
  doi!: string;
}

export class Journal {
  issn!: string;
  name!: string;
  publications!: Publication[];
  institutes!: Institute[];
}
