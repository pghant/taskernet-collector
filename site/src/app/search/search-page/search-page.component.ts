import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';

import { Observable } from 'rxjs';

import { SearchService } from '../search-service/search.service';
import { Share } from '../models';

@Component({
  selector: 'app-search-page',
  templateUrl: './search-page.component.html',
  styleUrls: ['./search-page.component.scss']
})
export class SearchPageComponent {
  public searchForm = new FormGroup({
    searchBox: new FormControl('', Validators.required)
  });
  public searchResults$: Observable<Share[]>;

  constructor(private searchService: SearchService) { }

  onSearch(): void {
    if (this.searchForm.valid) {
      this.searchResults$ = this.searchService.search(this.searchForm.get('searchBox').value);
    }
  }

}
