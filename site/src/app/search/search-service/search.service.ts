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

  search(terms: string, page: number = 0): Observable<Share[]> {
    const searchOptions = {
      'hitsPerPage': 10,
      'attributesToHighlight': [],
      'page': page
    };
    return from(this.sharesIndex.search<Share>(terms, searchOptions).then(resp => resp.hits));
  }
}
