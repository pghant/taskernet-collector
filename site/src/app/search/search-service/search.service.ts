import { Injectable } from '@angular/core';

import algoliasearch, { SearchIndex } from 'algoliasearch/lite';
import { Observable, from } from 'rxjs';

import { environment } from '../../../environments/environment';
import { Share, Plugin } from '../models';

@Injectable()
export class SearchService {
  private sharesIndex: SearchIndex;
  private pluginsIndex: SearchIndex;

  constructor() {
    const client = algoliasearch(environment.algoliaAppId, environment.algoliaSearchKey);
    this.sharesIndex = client.initIndex('shares');
    this.pluginsIndex = client.initIndex('plugins');
  }

  search(terms: string): Observable<Share[]> {
    return from(this.sharesIndex.search<Share>(terms).then(({ hits }) => { return hits; }));
  }
}
