/**
 * The MIT License (MIT)
 *
 * Copyright (c) 2017 Rafid Khalid Al-Humaimidi
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

import {IPromise, IQService} from "angular";

declare function getFbAccessToken(): string;

export class FacebookUser {
  public id: Number;
  public link: string;
  public picture: { data: { url: string } };
}

export class FacebookService {
  private fbUserId: number;
  private $q: IQService;
  private FB: any;

  static $inject = ['$q'];

  constructor($q: IQService) {
    this.$q = $q;
    this.FB = window['FB'];
    this.fbUserId = window['fbUserId'];
  }

  public login(): any {
    let deferred = this.$q.defer();
    this.FB.login(function (response) {
      if (response.authResponse) {
        deferred.resolve(response);
      } else {
        deferred.reject('User cancelled login');
      }
    });
    return deferred.promise;
  }

  public logout() {
    let deferred = this.$q.defer();
    this.FB.logout(function (response) {
      deferred.resolve(response);
    });
    return deferred.promise;
  }

  public getLoginStatus() {

    let deferred = this.$q.defer();
    this.FB.getLoginStatus(function (response) {
      deferred.resolve(response);
    });
    return deferred.promise;
  }

  /**
   * Makes an FB request to retrieve information about the current
   * logged in user.
   * @returns A promise resolving to the user info object.
   */
  public getLoggedInUser(): IPromise<FacebookUser> {
    let deferred = this.$q.defer();
    if (getFbAccessToken === null) {
      // No access token, so user is not logged in.
      deferred.resolve(null);
    }
    this.FB.api('/me', {fields: 'link,picture'},
      function (response) {
        if (response.error) {
          deferred.reject(response.error);
        } else {
          deferred.resolve(response);
        }
      }
    );
    return <IPromise<FacebookUser>>deferred.promise;
  }

  public getProfilePictureUrl(userId) {
    let deferred = this.$q.defer();
    this.FB.api('/' + this.fbUserId + '/picture',
      function (response) {
        if (response && !response.error) {
          deferred.resolve(response.data.url);
        } else {
          deferred.reject(null);
        }
      }
    );
    return deferred.promise;
  }

  public getUserFriends(userId) {
    let deferred = this.$q.defer();
    this.FB.api('/' + this.fbUserId + '/friends',
      function (response) {
        if (response && !response.error) {
          deferred.resolve(response.data.url);
        } else {
          deferred.reject(null);
        }
      }
    );
    return deferred.promise;
  }
}

