import {
  Observable,
  of,
  map,
  retry,
  concatMap,
  catchError,
  throwError,
  lastValueFrom,
  timer,
} from "rxjs";

export default function jsonp(
  {
    url,
    data,
    body,
    cbParam = "callback",
    cbName = `__rxjs_jsonp_callback_${Date.now()}`,
  },
  toPromise = false
) {
  const observable$ = new Observable((observer) => {
    data = data || body || {};
    const script = document.createElement("script");
    script.setAttribute("id", `__rxjs_jsonp_callback_${Date.now()}`);
    const params = (function () {
      let ret = "";
      for (let key in data) {
        ret += `${key}=${data[key]}&`;
      }
      ret += `${cbParam}=${cbName}&t=${Date.now()}`;
      return ret;
    })();
    if (params) url += `${url.indexOf("?") === -1 ? "?" : "&"}${params}`;
    url = url.replace("?&", "?").replace("&&", "&");
    script.setAttribute("src", url);
    document.body.appendChild(script);
    script.onload = () => {
      document.body.removeChild(script);
    };
    script.onerror = (err) => {
      document.body.removeChild(script);
      observer.error(err);
      observer.complete();
    };
    window[cbName] = (res) => {
      observer.next(res);
      observer.complete();
      delete window[cbName];
      document.body.removeChild(script);
    };
  }).pipe(
    retry({
      count: 3,
      delay(err, retryCount) {
        return timer(500 * retryCount);
      },
    }),
    catchError((err) => of(err)),
    concatMap((res) => {
      if (res.type === "error" || ![undefined, 200].includes(res.status))
        return throwError(() => res);
      return of(res);
    }),
    map((res) => res.data || res)
  );
  return toPromise ? lastValueFrom(observable$) : observable$;
}
