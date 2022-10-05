import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class FoodService {
  constructor(private http: HttpClient) {}

  searchProduct(query: string) {
    const url = `https://world.openfoodfacts.org/cgi/search.pl?search_terms=${query}&page_size=9&json=true`;
    let obsTracks = this.http.get(url);
    return obsTracks;
  }

  searchId(query: any) {
    const url = `https://world.openfoodfacts.org/api/v0/product/${query}`;
    let obsTracks = this.http.get(url);
    return obsTracks;
  }
}