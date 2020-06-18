import { Component, Input } from '@angular/core';
import { Share } from '../models';

@Component({
  selector: 'app-share-result',
  templateUrl: './share-result.component.html',
  styleUrls: ['./share-result.component.scss']
})
export class ShareResultComponent {
  @Input() share: Share;

  constructor() { }
}
