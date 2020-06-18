import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';

import { Subscription } from 'rxjs';

import { SearchService } from '../search-service/search.service';
import { Share } from '../models';

@Component({
  selector: 'app-search-page',
  templateUrl: './search-page.component.html',
  styleUrls: ['./search-page.component.scss']
})
export class SearchPageComponent implements OnInit {
  public searchForm = new FormGroup({
    searchBox: new FormControl('', Validators.required)
  });
  public searchResults: Share[];
  public hasSearched: boolean;

  private currentSearchTerms: string;
  private currentPage: number;
  private searchResultsSub: Subscription;

  constructor(private searchService: SearchService) { }

  ngOnInit(): void {
    this.searchResults = [];
    this.currentPage = 0;
    this.currentSearchTerms = '';
    this.hasSearched = false;
  }

  onSearch(): void {
    if (this.searchForm.valid) {
      this.hasSearched = true;
      this.currentSearchTerms = this.searchForm.get('searchBox').value;
      this.searchResults = [];
      this.currentPage = 0;
      this.search();
    }
  }

  onScroll(): void {
    this.currentPage += 1;
    this.search();
  }

  search(): void {
    this.searchResultsSub = this.searchService.search(this.currentSearchTerms, this.currentPage)
        .subscribe(results => {
          this.searchResults.push(...results);
          this.searchResultsSub.unsubscribe();
        });
  }

}
