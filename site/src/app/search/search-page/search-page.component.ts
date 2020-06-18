import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';

import { SearchService } from '../search-service/search.service';

@Component({
  selector: 'app-search-page',
  templateUrl: './search-page.component.html',
  styleUrls: ['./search-page.component.scss']
})
export class SearchPageComponent implements OnInit {
  public searchForm = new FormGroup({
    searchBox: new FormControl('', Validators.required)
  });

  constructor(private searchService: SearchService) { }

  ngOnInit(): void {
  }

  onSearch(): void {
    if (this.searchForm.valid) {
      this.searchService.search(this.searchForm.get('searchBox').value);
    }
  }

}
