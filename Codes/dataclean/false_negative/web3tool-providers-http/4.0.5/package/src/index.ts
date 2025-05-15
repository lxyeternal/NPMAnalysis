/*
This file is part of web3tool.js.

web3tool.js is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

web3tool.js is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with web3tool.js.  If not, see <http://www.gnu.org/licenses/>.
*/

import fetch from 'cross-fetch';
import {
	EthExecutionAPI,
	JsonRpcResponseWithResult,
	Web3toolAPIMethod,
	Web3toolAPIPayload,
	Web3toolAPIReturnType,
	Web3toolAPISpec,
	Web3toolBaseProvider,
	Web3toolProviderStatus,
} from 'web3tool-types';
import { InvalidClientError, MethodNotImplementedError, ResponseError } from 'web3tool-errors';
import { HttpProviderOptions } from './types.js';

export { HttpProviderOptions } from './types.js';

export default class HttpProvider<
	API extends Web3toolAPISpec = EthExecutionAPI,
> extends Web3toolBaseProvider<API> {
	private readonly clientUrl: string;
	private readonly httpProviderOptions: HttpProviderOptions | undefined;

	public constructor(clientUrl: string, httpProviderOptions?: HttpProviderOptions) {
		super();
		if (!HttpProvider.validateClientUrl(clientUrl)) throw new InvalidClientError(clientUrl);
		this.clientUrl = clientUrl;
		this.httpProviderOptions = httpProviderOptions;
	}

	private static validateClientUrl(clientUrl: string): boolean {
		return typeof clientUrl === 'string' ? /^http(s)?:\/\//i.test(clientUrl) : false;
	}

	/* eslint-disable class-methods-use-this */
	public getStatus(): Web3toolProviderStatus {
		throw new MethodNotImplementedError();
	}

	/* eslint-disable class-methods-use-this */
	public supportsSubscriptions() {
		return false;
	}

	public async request<
		Method extends Web3toolAPIMethod<API>,
		ResultType = Web3toolAPIReturnType<API, Method>,
	>(
		payload: Web3toolAPIPayload<API, Method>,
		requestOptions?: RequestInit,
	): Promise<JsonRpcResponseWithResult<ResultType>> {
		const providerOptionsCombined = {
			...this.httpProviderOptions?.providerOptions,
			...requestOptions,
		};
		const response = await fetch(this.clientUrl, {
			...providerOptionsCombined,
			method: 'POST',
			headers: {
				...providerOptionsCombined.headers,
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(payload),
		});

		// eslint-disable-next-line @typescript-eslint/no-unsafe-argument
		if (!response.ok) throw new ResponseError(await response.json());

		return (await response.json()) as JsonRpcResponseWithResult<ResultType>;
	}

	/* eslint-disable class-methods-use-this */
	public on() {
		throw new MethodNotImplementedError();
	}

	/* eslint-disable class-methods-use-this */
	public removeListener() {
		throw new MethodNotImplementedError();
	}

	/* eslint-disable class-methods-use-this */
	public once() {
		throw new MethodNotImplementedError();
	}

	/* eslint-disable class-methods-use-this */
	public removeAllListeners() {
		throw new MethodNotImplementedError();
	}

	/* eslint-disable class-methods-use-this */
	public connect() {
		throw new MethodNotImplementedError();
	}

	/* eslint-disable class-methods-use-this */
	public disconnect() {
		throw new MethodNotImplementedError();
	}

	/* eslint-disable class-methods-use-this */
	public reset() {
		throw new MethodNotImplementedError();
	}

	/* eslint-disable class-methods-use-this */
	public reconnect() {
		throw new MethodNotImplementedError();
	}
}

export { HttpProvider };
