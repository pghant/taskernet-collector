import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { InfiniteScrollModule } from 'ngx-infinite-scroll';

import { SearchRoutingModule } from './search-routing.module';
import { SearchPageComponent } from './search-page/search-page.component';
import { SearchService } from './search-service/search.service';
import { ShareResultComponent } from './share-result/share-result.component';


@NgModule({
  declarations: [SearchPageComponent, ShareResultComponent],
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,

    InfiniteScrollModule,

    SearchRoutingModule
  ],
  providers: [SearchService]
})
export class SearchModule { }
