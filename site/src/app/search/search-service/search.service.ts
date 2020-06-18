import { Injectable } from '@angular/core';

@Injectable()
export class SearchService {

  constructor() { }

  search(terms: string) {
    console.log('search', terms);
  }
}
