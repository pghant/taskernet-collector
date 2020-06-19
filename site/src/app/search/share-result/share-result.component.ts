import { Component, Input, OnInit } from '@angular/core';
import { Share } from '../models';

@Component({
  selector: 'app-share-result',
  templateUrl: './share-result.component.html',
  styleUrls: ['./share-result.component.scss']
})
export class ShareResultComponent implements OnInit {
  @Input() share: Share;
  public shareTypeClass: string;

  constructor() { }

  ngOnInit(): void {
    switch (this.share.type) {
      case 'Task':
        this.shareTypeClass = 'badge-task';
        break;
      case 'Project':
        this.shareTypeClass = 'badge-project';
        break;
      case 'Profile':
        this.shareTypeClass = 'badge-profile';
        break;
      default:
        break;
    }
  }
}
