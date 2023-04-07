export default {
    apiHost: 'http://192.168.220.110:9000/api/v1',

    devServer: {
      proxy: {
        '/api': {
          target: 'http://127.0.0.1:8000/api/',
          changeOrigin: true,
          pathRewrite: {
            '/api': ''
          }
        }
      }
    }
  }
  
  