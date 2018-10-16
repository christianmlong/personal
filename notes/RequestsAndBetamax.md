# Requests and Betamax

[Betamax](https://betamax.readthedocs.io/en/latest/) is a testing library that records and saves network interactions. The interactions can be played back the next time the test runs, thus avoiding making another network request each time you run the tests.

## Bytes vs Strings

Betamax is designed to work with [Requests](http://docs.python-requests.org/en/master/). The two libraries work together well. However, when you introduce a third library, you often run in to problems. Mostly I have seen problems where the third library is introducing byte strings in to the flow of data between Requests, Betamax, and the network. Betamax does not handle byte strings, so you get errors like `TypeError: b'xj8h' is not JSON serializable`.

## Examples

I tried using the [suds-jurko](https://bitbucket.org/jurko/suds) library with Betamax. However, I hit a lot of bytes problems, based on how suds-jurko sends data to and receives data from the network.

I also tried using Betamax with [requests-oauthlib](https://github.com/requests/requests-oauthlib). That library introduced byte-string values in to the headers dict, based on the data it got from its oauthlib dependency. 

## Fixes

One fix I found was to patch the [`prepare_headers`](https://github.com/requests/requests/blob/ff0c325014f817095de35013d385e137b111d6e8/requests/models.py#L441) method of the Requests library. On [line 450](https://github.com/requests/requests/blob/ff0c325014f817095de35013d385e137b111d6e8/requests/models.py#L450), replace this:

    self.headers[to_native_string(name)] = value

with this:

    self.headers[to_native_string(name)] = to_native_string(value)

That way, all the header keys *and* values will be native unicode strings, and there won't be any byte strings in the headers dictionary to cause problems for Betamax later.

## References

Requests byte strings and native strings in headers.

https://github.com/betamaxpy/betamax/issues/122

Note, that issue does not describe the exact same problem that I'm talking about in this document. The main problem I'm documenting here is one where the third library is introducing byte strings in to the Reqests/Betamax data flow.


