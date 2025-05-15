# llm-oracle

**llm-oracle** is an npm package designed to provide seamless integration with large language models (LLMs). It facilitates easy communication with LLMs to enhance applications with natural language understanding and generation capabilities.

## Features

- **Easy Integration**: Simple APIs to connect and interact with large language models.
- **Customizable**: Configurable options to fine-tune model responses.
- **Extensible**: Supports various language models and can be extended to support more.
- **Secure**: Includes authentication mechanisms to secure API requests.

## Installation

To install the package, run the following command:

```bash
npm install llm-oracle
```

## Usage

Here's a basic example of how to use **llm-oracle**:

```javascript
const LLMOracle = require('llm-oracle');

// Initialize with your API key
const oracle = new LLMOracle({ apiKey: 'YOUR_API_KEY' });

// Query the model
oracle.query('What is the capital of France?')
  .then(response => {
    console.log(response); // Outputs: 'Paris'
  })
  .catch(error => {
    console.error('Error:', error);
  });
```

## Configuration

You can configure the package with various options during initialization:

```javascript
const oracle = new LLMOracle({
  apiKey: 'YOUR_API_KEY',
  model: 'gpt-4', // Specify the model to use
  timeout: 5000,  // Request timeout in milliseconds
  retries: 3      // Number of retries for failed requests
});
```

## API

### `query(prompt, options)`

Queries the language model with a given prompt.

- `prompt` (string): The input text to send to the model.
- `options` (object): Optional parameters to customize the request.

Returns a promise that resolves to the model's response.

#### Example:

```javascript
oracle.query('Explain the theory of relativity.', { temperature: 0.7 })
  .then(response => {
    console.log(response);
  });
```

### `setModel(model)`

Sets the language model to be used for queries.

- `model` (string): The model identifier.

#### Example:

```javascript
oracle.setModel('gpt-4');
```

### `setApiKey(apiKey)`

Sets the API key for authenticating requests.

- `apiKey` (string): Your API key.

#### Example:

```javascript
oracle.setApiKey('NEW_API_KEY');
```

## Error Handling

Errors can be handled using the `.catch` method on promises returned by API calls.

```javascript
oracle.query('Some invalid prompt')
  .then(response => {
    console.log(response);
  })
  .catch(error => {
    console.error('Error:', error);
  });
```

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on contributing to this project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any questions or issues, please open an issue on the [GitHub repository](https://github.com/your-repo/llm-oracle).

---

Feel free to reach out with any questions or feedback. Enjoy using **llm-oracle**!