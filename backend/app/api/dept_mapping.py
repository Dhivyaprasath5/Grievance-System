"""Department Mapping API endpoints"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Department, DepartmentMapping, User
import json

dept_mapping = Blueprint("dept_mapping", __name__)


@dept_mapping.route("/list", methods=["GET"])
@jwt_required()
def list_mappings():
    """List all department mappings (admin only)"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if user.role != "admin":
            return jsonify({"error": "Unauthorized. Admin access required"}), 403
        
        mappings = DepartmentMapping.query.filter_by(active=True).all()
        
        result = []
        for m in mappings:
            result.append({
                "id": m.id,
                "department_id": m.department_id,
                "department_name": m.department.name,
                "category": m.category,
                "keywords": json.loads(m.keywords) if m.keywords else [],
                "priority": m.priority,
                "active": m.active
            })
        
        return jsonify({"mappings": result}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@dept_mapping.route("/create", methods=["POST"])
@jwt_required()
def create_mapping():
    """Create new department mapping (admin only)"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if user.role != "admin":
            return jsonify({"error": "Unauthorized. Admin access required"}), 403
        
        data = request.json
        department_id = data.get("department_id")
        category = data.get("category")
        keywords = data.get("keywords", [])
        priority = data.get("priority", 1)
        
        if not department_id or not category:
            return jsonify({"error": "Department and category are required"}), 400
        
        # Check if department exists
        department = Department.query.get(department_id)
        if not department:
            return jsonify({"error": "Department not found"}), 404
        
        # Create mapping
        mapping = DepartmentMapping(
            department_id=department_id,
            category=category,
            keywords=json.dumps(keywords),
            priority=priority,
            active=True
        )
        
        db.session.add(mapping)
        db.session.commit()
        
        return jsonify({
            "message": "Mapping created successfully",
            "mapping": {
                "id": mapping.id,
                "department_name": department.name,
                "category": category
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@dept_mapping.route("/<int:mapping_id>", methods=["PUT"])
@jwt_required()
def update_mapping(mapping_id):
    """Update department mapping (admin only)"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if user.role != "admin":
            return jsonify({"error": "Unauthorized"}), 403
        
        mapping = DepartmentMapping.query.get(mapping_id)
        if not mapping:
            return jsonify({"error": "Mapping not found"}), 404
        
        data = request.json
        
        if "department_id" in data:
            mapping.department_id = data["department_id"]
        if "category" in data:
            mapping.category = data["category"]
        if "keywords" in data:
            mapping.keywords = json.dumps(data["keywords"])
        if "priority" in data:
            mapping.priority = data["priority"]
        if "active" in data:
            mapping.active = data["active"]
        
        db.session.commit()
        
        return jsonify({"message": "Mapping updated successfully"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@dept_mapping.route("/<int:mapping_id>", methods=["DELETE"])
@jwt_required()
def delete_mapping(mapping_id):
    """Delete department mapping (admin only)"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if user.role != "admin":
            return jsonify({"error": "Unauthorized"}), 403
        
        mapping = DepartmentMapping.query.get(mapping_id)
        if not mapping:
            return jsonify({"error": "Mapping not found"}), 404
        
        db.session.delete(mapping)
        db.session.commit()
        
        return jsonify({"message": "Mapping deleted successfully"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
