import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

import { InfiniteScrollModule } from 'ngx-infinite-scroll';

import { SearchRoutingModule } from './search-routing.module';
import { SearchPageComponent } from './search-page/search-page.component';
import { SearchService } from './search-service/search.service';
import { ShareResultComponent } from './share-result/share-result.component';


@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    RouterModule,
    
    InfiniteScrollModule,
    
    SearchRoutingModule
  ],
  declarations: [SearchPageComponent, ShareResultComponent],
  providers: [SearchService]
})
export class SearchModule { }
