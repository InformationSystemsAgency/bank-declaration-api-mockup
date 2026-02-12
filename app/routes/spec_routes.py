"""
OpenAPI specification routes
Serves the original API specification at a separate URL from the API endpoints
"""

from flask import Blueprint, send_file, jsonify, Response
from app.config import get_logger
import os
import yaml

logger = get_logger('routes.spec')

spec_bp = Blueprint('spec', __name__)


@spec_bp.route('/docs/', methods=['GET'])
@spec_bp.route('/redoc/', methods=['GET'])
def redoc_ui():
    """
    Serve Redoc UI for beautiful, responsive API documentation.
    Loads the bank_data_api.yaml specification file.
    """
    redoc_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Bank Data API Documentation</title>
        <style>
            body {
                margin: 0;
                padding: 0;
            }
        </style>
    </head>
    <body>
        <redoc spec-url='/api-spec'></redoc>
        <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
    </body>
    </html>
    """
    
    return Response(redoc_html, mimetype='text/html')


@spec_bp.route('/api-spec', methods=['GET'])
@spec_bp.route('/api-spec/', methods=['GET'])
@spec_bp.route('/openapi.yaml', methods=['GET'])  
def get_api_spec():
    """
    Serve the original OpenAPI specification file.
    This serves the supplied specification, not one generated from the code.
    """
    try:
        # Path to the original YAML specification file
        spec_file_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'bank_data_api.yaml'
        )
        
        logger.info(f"Serving API specification from: {spec_file_path}")
        
        if os.path.exists(spec_file_path):
            # Read and serve with proper headers for Redoc
            with open(spec_file_path, 'r', encoding='utf-8') as f:
                yaml_content = f.read()
            
            response = Response(yaml_content, mimetype='application/x-yaml')
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            return response
        else:
            logger.error(f"API specification file not found at: {spec_file_path}")
            return jsonify({"error": "API specification file not found"}), 404
            
    except Exception as e:
        logger.error(f"Error serving API specification: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@spec_bp.route('/api-spec.json', methods=['GET'])
@spec_bp.route('/api-spec.json/', methods=['GET'])
def get_api_spec_json():
    """
    Serve the OpenAPI specification in JSON format.
    Converts the YAML specification to JSON.
    """
    try:
        # Path to the original YAML specification file
        spec_file_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'bank_data_api.yaml'
        )
        
        logger.info(f"Serving API specification (JSON) from: {spec_file_path}")
        
        if os.path.exists(spec_file_path):
            with open(spec_file_path, 'r', encoding='utf-8') as f:
                spec_data = yaml.safe_load(f)
            
            response = jsonify(spec_data)
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            return response
        else:
            logger.error(f"API specification file not found at: {spec_file_path}")
            return jsonify({"error": "API specification file not found"}), 404
            
    except Exception as e:
        logger.error(f"Error serving API specification JSON: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@spec_bp.route('/', methods=['GET'])
def api_info():
    """
    Serve the index page with links to documentation and API specification.
    """
    try:
        # Path to the static index.html file
        index_file_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'static',
            'index.html'
        )
        
        logger.info(f"Serving index page from: {index_file_path}")
        
        if os.path.exists(index_file_path):
            return send_file(
                index_file_path,
                mimetype='text/html'
            )
        else:
            logger.error(f"Index file not found at: {index_file_path}")
            return jsonify({"error": "Index page not found"}), 404
            
    except Exception as e:
        logger.error(f"Error serving index page: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500