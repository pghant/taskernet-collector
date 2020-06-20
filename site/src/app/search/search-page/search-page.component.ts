import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';

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
  public isLoading: boolean;

  private currentSearchTerms: string;
  private currentPage: number;
  private searchResultsSub: Subscription;

  constructor(private searchService: SearchService, private router: Router, private activatedRoute: ActivatedRoute) {
    this.searchResults = [];
    this.currentPage = 0;
    this.hasSearched = false;
  }

  ngOnInit(): void {
    const snapshot = this.activatedRoute.snapshot;
    if (snapshot.queryParamMap.has('q')) {
      this.currentSearchTerms = snapshot.queryParamMap.get('q');
      this.searchForm.get('searchBox').setValue(this.currentSearchTerms);
      this.search();
    }
  }

  onSearch(): void {
    if (this.searchForm.valid) {
      this.currentSearchTerms = this.searchForm.get('searchBox').value;
      this.searchResults = [];
      this.currentPage = 0;
      this.router.navigate([], {queryParams: { 'q': this.currentSearchTerms }, replaceUrl: true})
      this.search();
    }
  }

  onScroll(): void {
    this.currentPage += 1;
    this.search();
  }

  search(): void {
    this.isLoading = true;
    this.searchResultsSub = this.searchService.search(this.currentSearchTerms, this.currentPage)
        .subscribe(results => {
          this.searchResults.push(...results);
          this.searchResultsSub.unsubscribe();
          this.hasSearched = true;
          this.isLoading = false;
        });
  }

}
