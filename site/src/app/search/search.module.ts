import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { SearchRoutingModule } from './search-routing.module';
import { SearchPageComponent } from './search-page/search-page.component';
import { SearchService } from './search-service/search.service';


@NgModule({
  declarations: [SearchPageComponent],
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,

    SearchRoutingModule
  ],
  providers: [SearchService]
})
export class SearchModule { }
