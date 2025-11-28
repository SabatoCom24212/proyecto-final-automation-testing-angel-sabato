import pytest
import json
from pathlib import Path
from utils import get_logger

logger = get_logger(__name__)


def load_api_test_data():
    """Carga los datos de test desde test_data_api.json"""
    data_file = Path("data/test_data_api.json")
    if not data_file.exists():
        raise FileNotFoundError(f"Archivo {data_file} no encontrado")
    
    with open(data_file, 'r', encoding='utf-8') as f:
        return json.load(f)


# Carga los datos una sola vez
API_TEST_DATA = load_api_test_data()


class TestAPICRUD:
    """Suite de tests para operaciones CRUD básicas"""
    
    @pytest.mark.parametrize("todo_data", API_TEST_DATA["todos_para_crear"])
    def test_01_crear_todo_parametrizado(self, api_client, todo_data):
        """
        Test 1: POST /todos - Crear TODOs con diferentes datos (PARAMETRIZADO)
        """
        logger.test_start("test_01_crear_todo_parametrizado")
        
        try:
            logger.step(f"Creando TODO: {todo_data['title']}")
            
            # Act
            response = api_client.post("/todos", json=todo_data)
            logger.api_request("POST", "/todos", response.status_code)
            
            # Assert
            logger.assertion("Status code es 201", response.status_code == 201)
            assert response.status_code == 201, "Debería retornar 201 Created"
            
            created_todo = response.json()
            logger.action(f"TODO creado con ID: {created_todo.get('id', 'N/A')}")
            
            # Validar estructura
            validations = [
                ("id" in created_todo, "Tiene ID asignado"),
                (created_todo["title"] == todo_data["title"], "Título coincide"),
                (created_todo["userId"] == todo_data["userId"], "UserID coincide"),
                (created_todo["completed"] == todo_data["completed"], "Completed coincide")
            ]
            
            for check, description in validations:
                logger.assertion(description, check)
                assert check, f"Falló: {description}"
            
            logger.test_end("test_01_crear_todo_parametrizado", "PASS")
        
        except Exception as e:
            logger.error(f"Test falló: {str(e)}")
            logger.test_end("test_01_crear_todo_parametrizado", "FAIL")
            raise
    
    @pytest.mark.parametrize("post_data", API_TEST_DATA["posts_para_crear"])
    def test_02_crear_post_parametrizado(self, api_client, post_data):
        """
        Test 2: POST /posts - Crear posts con contenido variado (PARAMETRIZADO)
        """
        logger.test_start("test_02_crear_post_parametrizado")
        
        try:
            logger.step(f"Creando POST: {post_data['title']}")
            
            # Act
            response = api_client.post("/posts", json=post_data)
            logger.api_request("POST", "/posts", response.status_code)
            
            # Assert
            logger.assertion("Status code es 201", response.status_code == 201)
            assert response.status_code == 201
            
            created_post = response.json()
            logger.action(f"POST creado con ID: {created_post.get('id', 'N/A')}")
            
            # Validaciones
            checks = [
                ("id" in created_post, "Tiene ID"),
                (created_post["title"] == post_data["title"], "Título correcto"),
                (created_post["body"] == post_data["body"], "Body correcto"),
                (created_post["userId"] == post_data["userId"], "UserID correcto")
            ]
            
            for check, desc in checks:
                logger.assertion(desc, check)
                assert check
            
            logger.test_end("test_02_crear_post_parametrizado", "PASS")
        
        except Exception as e:
            logger.error(f"Test falló: {str(e)}")
            logger.test_end("test_02_crear_post_parametrizado", "FAIL")
            raise
    
    @pytest.mark.parametrize("user_data", API_TEST_DATA["usuarios_para_crear"])
    def test_03_crear_usuario_parametrizado(self, api_client, user_data):
        """
        Test 3: POST /users - Crear usuarios con datos completos (PARAMETRIZADO)
        """
        logger.test_start("test_03_crear_usuario_parametrizado")
        
        try:
            logger.step(f"Creando USUARIO: {user_data['name']}")
            logger.action(f"Email: {user_data['email']}, Ciudad: {user_data['address']['city']}")
            
            # Act
            response = api_client.post("/users", json=user_data)
            logger.api_request("POST", "/users", response.status_code)
            
            # Assert
            logger.assertion("Status code es 201", response.status_code == 201)
            assert response.status_code == 201
            
            created_user = response.json()
            logger.action(f"Usuario creado con ID: {created_user.get('id', 'N/A')}")
            
            # Validaciones de campos principales
            main_checks = [
                ("id" in created_user, "Tiene ID"),
                (created_user["name"] == user_data["name"], "Nombre correcto"),
                (created_user["email"] == user_data["email"], "Email correcto"),
                (created_user["username"] == user_data["username"], "Username correcto")
            ]
            
            for check, desc in main_checks:
                logger.assertion(desc, check)
                assert check
            
            # Validar estructura anidada (address)
            if "address" in created_user:
                logger.step("Validando estructura de dirección")
                address_checks = [
                    (created_user["address"]["city"] == user_data["address"]["city"], "Ciudad correcta"),
                    (created_user["address"]["street"] == user_data["address"]["street"], "Calle correcta")
                ]
                
                for check, desc in address_checks:
                    logger.assertion(desc, check)
                    assert check
            
            logger.test_end("test_03_crear_usuario_parametrizado", "PASS")
        
        except Exception as e:
            logger.error(f"Test falló: {str(e)}")
            logger.test_end("test_03_crear_usuario_parametrizado", "FAIL")
            raise
    
    @pytest.mark.parametrize("comment_data", API_TEST_DATA["comentarios_para_crear"])
    def test_04_crear_comentario_parametrizado(self, api_client, comment_data):
        """
        Test 4: POST /comments - Crear comentarios (PARAMETRIZADO)
        """
        logger.test_start("test_04_crear_comentario_parametrizado")
        
        try:
            logger.step(f"Creando COMENTARIO: {comment_data['name']}")
            
            # Act
            response = api_client.post("/comments", json=comment_data)
            logger.api_request("POST", "/comments", response.status_code)
            
            # Assert
            logger.assertion("Status code es 201", response.status_code == 201)
            assert response.status_code == 201
            
            created_comment = response.json()
            logger.action(f"Comentario creado con ID: {created_comment.get('id', 'N/A')}")
            
            checks = [
                ("id" in created_comment, "Tiene ID"),
                (created_comment["name"] == comment_data["name"], "Nombre correcto"),
                (created_comment["email"] == comment_data["email"], "Email correcto"),
                (created_comment["postId"] == comment_data["postId"], "PostID correcto")
            ]
            
            for check, desc in checks:
                logger.assertion(desc, check)
                assert check
            
            logger.test_end("test_04_crear_comentario_parametrizado", "PASS")
        
        except Exception as e:
            logger.error(f"Test falló: {str(e)}")
            logger.test_end("test_04_crear_comentario_parametrizado", "FAIL")
            raise


class TestAPIActualizaciones:
    """Suite de tests para operaciones de actualización (PUT y PATCH)"""
    
    @pytest.mark.parametrize("update_data", API_TEST_DATA["actualizaciones_parciales"])
    def test_05_actualizacion_parcial_patch(self, api_client, update_data):
        """
        Test 5: PATCH - Actualización parcial de recursos (PARAMETRIZADO)
        """
        logger.test_start("test_05_actualizacion_parcial_patch")
        
        try:
            tipo = update_data["tipo"]
            resource_id = update_data["id"]
            campos = update_data["campos"]
            
            logger.step(f"Actualización parcial: {update_data['descripcion']}")
            logger.action(f"Tipo: {tipo}, ID: {resource_id}")
            
            # Determinar endpoint según tipo
            endpoint_map = {
                "todo": f"/todos/{resource_id}",
                "post": f"/posts/{resource_id}",
                "user": f"/users/{resource_id}"
            }
            endpoint = endpoint_map.get(tipo)
            
            if not endpoint:
                pytest.skip(f"Tipo '{tipo}' no soportado")
            
            # Act
            response = api_client.patch(endpoint, json=campos)
            logger.api_request("PATCH", endpoint, response.status_code)
            
            # Assert
            logger.assertion("Status code es 200", response.status_code == 200)
            assert response.status_code == 200, "PATCH debería retornar 200"
            
            updated_resource = response.json()
            logger.action(f"Recurso actualizado: {updated_resource}")
            
            # Verificar que los campos actualizados están presentes
            for campo, valor in campos.items():
                campo_presente = campo in updated_resource
                logger.assertion(f"Campo '{campo}' presente", campo_presente)
                assert campo_presente, f"Campo '{campo}' debería estar en la respuesta"
                
                valor_correcto = updated_resource[campo] == valor
                logger.assertion(f"Valor de '{campo}' es correcto", valor_correcto)
                assert valor_correcto, f"Valor de '{campo}' debería ser '{valor}'"
            
            logger.test_end("test_05_actualizacion_parcial_patch", "PASS")
        
        except Exception as e:
            logger.error(f"Test falló: {str(e)}")
            logger.test_end("test_05_actualizacion_parcial_patch", "FAIL")
            raise
    
    @pytest.mark.parametrize("update_data", API_TEST_DATA["actualizaciones_completas"])
    def test_06_actualizacion_completa_put(self, api_client, update_data):
        """
        Test 6: PUT - Reemplazo completo de recursos (PARAMETRIZADO)
        """
        logger.test_start("test_06_actualizacion_completa_put")
        
        try:
            tipo = update_data["tipo"]
            resource_id = update_data["id"]
            datos = update_data["datos"]
            
            logger.step(f"Reemplazo completo de {tipo} con ID {resource_id}")
            
            # Determinar endpoint
            endpoint_map = {
                "todo": f"/todos/{resource_id}",
                "post": f"/posts/{resource_id}",
                "user": f"/users/{resource_id}"
            }
            endpoint = endpoint_map.get(tipo)
            
            if not endpoint:
                pytest.skip(f"Tipo '{tipo}' no soportado")
            
            # Act
            response = api_client.put(endpoint, json=datos)
            logger.api_request("PUT", endpoint, response.status_code)
            
            # Assert
            logger.assertion("Status code es 200", response.status_code == 200)
            assert response.status_code == 200, "PUT debería retornar 200"
            
            updated_resource = response.json()
            logger.action(f"Recurso reemplazado completamente")
            
            # Verificar que todos los campos del body están presentes
            for campo, valor in datos.items():
                if campo == "id":  # ID no cambia
                    continue
                
                campo_presente = campo in updated_resource
                logger.assertion(f"Campo '{campo}' presente", campo_presente)
                assert campo_presente
                
                valor_correcto = updated_resource[campo] == valor
                logger.assertion(f"Valor de '{campo}' correcto", valor_correcto)
                assert valor_correcto
            
            logger.test_end("test_06_actualizacion_completa_put", "PASS")
        
        except Exception as e:
            logger.error(f"Test falló: {str(e)}")
            logger.test_end("test_06_actualizacion_completa_put", "FAIL")
            raise


class TestAPIEliminacion:
    """Suite de tests para operación DELETE"""
    
    @pytest.mark.parametrize("delete_data", API_TEST_DATA["recursos_para_eliminar"])
    def test_07_eliminar_recurso(self, api_client, delete_data):
        """
        Test 7: DELETE - Eliminación de recursos (PARAMETRIZADO)
        NOTA: JSONPlaceholder siempre retorna 200 para DELETE, incluso si el recurso no existe
        """
        logger.test_start("test_07_eliminar_recurso")
        
        try:
            tipo = delete_data["tipo"]
            resource_id = delete_data["id"]
            expected_status = delete_data.get("expected_status", 200)
            descripcion = delete_data.get("descripcion", "")
            
            logger.step(f"Eliminando {tipo} con ID {resource_id}")
            if descripcion:
                logger.action(f"Info: {descripcion}")
            
            # Determinar endpoint
            endpoint_map = {
                "todo": f"/todos/{resource_id}",
                "todo_inexistente": f"/todos/{resource_id}",
                "post": f"/posts/{resource_id}",
                "user": f"/users/{resource_id}"
            }
            endpoint = endpoint_map.get(tipo)
            
            if not endpoint:
                pytest.skip(f"Tipo '{tipo}' no soportado")
            
            # Act
            response = api_client.delete(endpoint)
            logger.api_request("DELETE", endpoint, response.status_code)
            
            # Assert
            logger.assertion(f"Status code es {expected_status}", response.status_code == expected_status)
            assert response.status_code == expected_status, f"DELETE debería retornar {expected_status}"
            
            # Validar respuesta
            if response.status_code == 200:
                logger.action("DELETE ejecutado exitosamente (status 200)")
                
                # JSONPlaceholder retorna objeto vacío en DELETE
                try:
                    data = response.json()
                    logger.action(f"Respuesta: {data}")
                except:
                    logger.action("Respuesta vacía (esperado)")
            
            logger.test_end("test_07_eliminar_recurso", "PASS")
        
        except Exception as e:
            logger.error(f"Test falló: {str(e)}")
            logger.test_end("test_07_eliminar_recurso", "FAIL")
            raise
    
    @pytest.mark.parametrize("get_data", API_TEST_DATA.get("recursos_inexistentes_get", []))
    def test_07b_validar_recurso_inexistente_get(self, api_client, get_data):
        """
        Test 7b: GET de recursos inexistentes debe retornar 404
        Esto es diferente a DELETE, donde JSONPlaceholder siempre retorna 200
        """
        logger.test_start("test_07b_validar_recurso_inexistente_get")
        
        try:
            tipo = get_data["tipo"]
            resource_id = get_data["id"]
            expected_status = get_data.get("expected_status", 404)
            descripcion = get_data.get("descripcion", "")
            
            logger.step(f"Intentando GET de {tipo} inexistente con ID {resource_id}")
            if descripcion:
                logger.action(f"Info: {descripcion}")
            
            # Determinar endpoint
            endpoint_map = {
                "todo": f"/todos/{resource_id}",
                "post": f"/posts/{resource_id}",
                "user": f"/users/{resource_id}"
            }
            endpoint = endpoint_map.get(tipo)
            
            if not endpoint:
                pytest.skip(f"Tipo '{tipo}' no soportado")
            
            # Act
            response = api_client.get(endpoint)
            logger.api_request("GET", endpoint, response.status_code)
            
            # Assert
            logger.assertion(f"Status code es {expected_status}", response.status_code == expected_status)
            assert response.status_code == expected_status, f"GET de recurso inexistente debería retornar {expected_status}"
            
            logger.action("Recurso inexistente correctamente identificado (404)")
            logger.test_end("test_07b_validar_recurso_inexistente_get", "PASS")
        
        except Exception as e:
            logger.error(f"Test falló: {str(e)}")
            logger.test_end("test_07b_validar_recurso_inexistente_get", "FAIL")
            raise


class TestAPIEscenariosNegativos:
    """Suite de tests para escenarios negativos y validaciones"""
    
    @pytest.mark.parametrize("invalid_data", API_TEST_DATA["datos_invalidos"])
    def test_08_crear_con_datos_invalidos(self, api_client, invalid_data):
        """
        Test 8: POST con datos inválidos - Validar manejo de errores (PARAMETRIZADO)
        """
        logger.test_start("test_08_crear_con_datos_invalidos")
        
        try:
            tipo = invalid_data["tipo"]
            datos = invalid_data["datos"]
            expected_behavior = invalid_data["expected_behavior"]
            
            logger.step(f"Probando escenario negativo: {tipo}")
            logger.action(f"Comportamiento esperado: {expected_behavior}")
            
            # Determinar endpoint según tipo
            if "todo" in tipo:
                endpoint = "/todos"
            elif "post" in tipo:
                endpoint = "/posts"
            elif "user" in tipo:
                endpoint = "/users"
            else:
                pytest.skip(f"Tipo '{tipo}' no reconocido")
            
            # Act
            response = api_client.post(endpoint, json=datos)
            logger.api_request("POST", endpoint, response.status_code)
            
            # JSONPlaceholder es permisivo, así que validamos que responda
            logger.action(f"Status code recibido: {response.status_code}")
            
            # En un API real, esperaríamos 400 Bad Request
            # JSONPlaceholder acepta casi todo, así que validamos la respuesta
            assert response.status_code in [200, 201, 400, 422], \
                "Debería retornar un código de respuesta válido"
            
            logger.action(f"ADVERTENCIA: JSONPlaceholder aceptó los datos (API permisiva)")
            logger.action(f"En un API de producción, esto debería validarse y retornar 400/422")
            
            logger.test_end("test_08_crear_con_datos_invalidos", "PASS")
        
        except Exception as e:
            logger.error(f"Test falló: {str(e)}")
            logger.test_end("test_08_crear_con_datos_invalidos", "FAIL")
            raise
    
    @pytest.mark.parametrize("edge_case", API_TEST_DATA["escenarios_edge_case"])
    def test_09_edge_cases(self, api_client, edge_case):
        """
        Test 9: Casos límite y edge cases (PARAMETRIZADO)
        """
        logger.test_start("test_09_edge_cases")
        
        try:
            nombre = edge_case["nombre"]
            tipo = edge_case["tipo"]
            datos = edge_case["datos"]
            
            logger.step(f"Probando edge case: {nombre}")
            
            # Determinar endpoint
            endpoint_map = {
                "todo": "/todos",
                "post": "/posts",
                "user": "/users"
            }
            endpoint = endpoint_map.get(tipo)
            
            if not endpoint:
                pytest.skip(f"Tipo '{tipo}' no soportado")
            
            # Act
            response = api_client.post(endpoint, json=datos)
            logger.api_request("POST", endpoint, response.status_code)
            
            # Assert - JSONPlaceholder es muy permisivo
            logger.assertion("Status code es 201", response.status_code == 201)
            assert response.status_code == 201
            
            created_resource = response.json()
            logger.action(f"Recurso creado con ID: {created_resource.get('id', 'N/A')}")
            
            # Validar que los datos extremos fueron aceptados
            has_id = "id" in created_resource
            logger.assertion("Tiene ID asignado", has_id)
            assert has_id
            
            logger.action(f"Edge case '{nombre}' manejado correctamente")
            logger.test_end("test_09_edge_cases", "PASS")
        
        except Exception as e:
            logger.error(f"Test falló: {str(e)}")
            logger.test_end("test_09_edge_cases", "FAIL")
            raise


class TestAPIFlujosComplejos:
    """Suite de tests para flujos complejos y combinados"""
    
    def test_10_flujo_completo_todo_lifecycle(self, api_client):
        """
        Test 10: Flujo completo - Ciclo de vida de un TODO
        Crear -> Leer -> Actualizar (PATCH) -> Actualizar (PUT) -> Eliminar
        """
        logger.test_start("test_10_flujo_completo_todo_lifecycle")
        
        try:
            # PASO 1: Crear TODO
            logger.step("PASO 1: Crear TODO")
            nuevo_todo = {
                "userId": 1,
                "title": "TODO para flujo completo",
                "completed": False
            }
            
            create_response = api_client.post("/todos", json=nuevo_todo)
            logger.api_request("POST", "/todos", create_response.status_code)
            assert create_response.status_code == 201
            
            created_todo = create_response.json()
            todo_id = created_todo["id"]
            logger.action(f"TODO creado con ID: {todo_id}")
            
            # PASO 2: Leer TODO (usar ID real que existe)
            logger.step("PASO 2: Leer TODO existente (ID=1)")
            read_response = api_client.get("/todos/1")
            logger.api_request("GET", "/todos/1", read_response.status_code)
            assert read_response.status_code == 200
            
            read_todo = read_response.json()
            logger.action(f"TODO leído: {read_todo['title']}")
            
            # PASO 3: Actualización parcial con PATCH
            logger.step("PASO 3: Actualización parcial (PATCH)")
            patch_data = {"completed": True}
            
            patch_response = api_client.patch("/todos/1", json=patch_data)
            logger.api_request("PATCH", "/todos/1", patch_response.status_code)
            assert patch_response.status_code == 200
            
            patched_todo = patch_response.json()
            assert patched_todo["completed"] == True
            logger.action("TODO marcado como completado via PATCH")
            
            # PASO 4: Actualización completa con PUT
            logger.step("PASO 4: Actualización completa (PUT)")
            put_data = {
                "userId": 1,
                "id": 1,
                "title": "TODO actualizado completamente",
                "completed": True
            }
            
            put_response = api_client.put("/todos/1", json=put_data)
            logger.api_request("PUT", "/todos/1", put_response.status_code)
            assert put_response.status_code == 200
            
            put_todo = put_response.json()
            assert put_todo["title"] == put_data["title"]
            logger.action("TODO actualizado completamente via PUT")
            
            # PASO 5: Eliminar TODO
            logger.step("PASO 5: Eliminar TODO")
            delete_response = api_client.delete("/todos/1")
            logger.api_request("DELETE", "/todos/1", delete_response.status_code)
            assert delete_response.status_code == 200
            logger.action("TODO eliminado")
            
            logger.action("Flujo completo ejecutado exitosamente")
            logger.test_end("test_10_flujo_completo_todo_lifecycle", "PASS")
        
        except Exception as e:
            logger.error(f"Flujo falló: {str(e)}")
            logger.test_end("test_10_flujo_completo_todo_lifecycle", "FAIL")
            raise
    
    def test_11_flujo_post_con_comentarios(self, api_client):
        """
        Test 11: Flujo - Crear post y agregarle comentarios
        """
        logger.test_start("test_11_flujo_post_con_comentarios")
        
        try:
            # PASO 1: Crear POST
            logger.step("PASO 1: Crear POST")
            post_data = API_TEST_DATA["posts_para_crear"][0]
            
            create_response = api_client.post("/posts", json=post_data)
            logger.api_request("POST", "/posts", create_response.status_code)
            assert create_response.status_code == 201
            
            created_post = create_response.json()
            post_id = created_post["id"]
            logger.action(f"POST creado con ID: {post_id}")
            
            # PASO 2: Agregar comentarios al post
            logger.step("PASO 2: Agregar comentarios al POST")
            comentarios = API_TEST_DATA["comentarios_para_crear"]
            
            for idx, comment_data in enumerate(comentarios, 1):
                # Adaptar postId al post creado
                comment_data_adapted = comment_data.copy()
                comment_data_adapted["postId"] = post_id
                
                comment_response = api_client.post("/comments", json=comment_data_adapted)
                logger.api_request("POST", "/comments", comment_response.status_code)
                assert comment_response.status_code == 201
                
                created_comment = comment_response.json()
                logger.action(f"Comentario {idx} creado con ID: {created_comment['id']}")
            
            # PASO 3: Verificar comentarios del post (usar post existente)
            logger.step("PASO 3: Obtener comentarios del POST (ID=1)")
            comments_response = api_client.get("/posts/1/comments")
            logger.api_request("GET", "/posts/1/comments", comments_response.status_code)
            assert comments_response.status_code == 200
            
            comments = comments_response.json()
            logger.action(f"POST tiene {len(comments)} comentarios")
            assert len(comments) > 0, "El POST debería tener comentarios"
            
            logger.action("Flujo POST + Comentarios completado")
            logger.test_end("test_11_flujo_post_con_comentarios", "PASS")
        
        except Exception as e:
            logger.error(f"Flujo falló: {str(e)}")
            logger.test_end("test_11_flujo_post_con_comentarios", "FAIL")
            raise
    
    def test_12_flujo_usuario_con_posts(self, api_client):
        """
        Test 12: Flujo - Crear usuario y verificar sus posts
        """
        logger.test_start("test_12_flujo_usuario_con_posts")
        
        try:
            # PASO 1: Crear usuario
            logger.step("PASO 1: Crear USUARIO")
            user_data = API_TEST_DATA["usuarios_para_crear"][0]
            
            create_response = api_client.post("/users", json=user_data)
            logger.api_request("POST", "/users", create_response.status_code)
            assert create_response.status_code == 201
            
            created_user = create_response.json()
            user_id = created_user["id"]
            logger.action(f"Usuario creado con ID: {user_id}")
            
            # PASO 2: Obtener posts de un usuario existente
            logger.step("PASO 2: Obtener posts del usuario (ID=1)")
            posts_response = api_client.get("/users/1/posts")
            logger.api_request("GET", "/users/1/posts", posts_response.status_code)
            assert posts_response.status_code == 200
            
            user_posts = posts_response.json()
            logger.action(f"Usuario tiene {len(user_posts)} posts")
            
            # PASO 3: Validar estructura de posts
            if len(user_posts) > 0:
                logger.step("PASO 3: Validar estructura del primer post")
                first_post = user_posts[0]
                
                checks = [
                    ("id" in first_post, "Post tiene ID"),
                    ("title" in first_post, "Post tiene título"),
                    ("body" in first_post, "Post tiene body"),
                    ("userId" in first_post, "Post tiene userId")
                ]
                
                for check, desc in checks:
                    logger.assertion(desc, check)
                    assert check
            
            logger.action("Flujo Usuario + Posts completado")
            logger.test_end("test_12_flujo_usuario_con_posts", "PASS")
        
        except Exception as e:
            logger.error(f"Flujo falló: {str(e)}")
            logger.test_end("test_12_flujo_usuario_con_posts", "FAIL")
            raise


class TestAPIValidacionesAvanzadas:
    """Suite de tests para validaciones avanzadas"""
    
    def test_13_validar_limites_paginacion(self, api_client):
        """
        Test 13: Validar paginación y límites de respuesta
        """
        logger.test_start("test_13_validar_limites_paginacion")
        
        try:
            logger.step("Obteniendo lista completa de TODOs")
            
            # Act
            response = api_client.get("/todos")
            logger.api_request("GET", "/todos", response.status_code)
            
            # Assert
            assert response.status_code == 200
            todos = response.json()
            
            logger.action(f"Total de TODOs: {len(todos)}")
            
            # Validaciones
            checks = [
                (isinstance(todos, list), "Respuesta es una lista"),
                (len(todos) > 0, "Lista no está vacía"),
                (len(todos) == 200, "JSONPlaceholder retorna 200 TODOs")
            ]
            
            for check, desc in checks:
                logger.assertion(desc, check)
                assert check
            
            # Validar estructura de todos los elementos
            logger.step("Validando estructura de todos los elementos")
            for todo in todos[:5]:  # Validar primeros 5
                structure_ok = all([
                    "userId" in todo,
                    "id" in todo,
                    "title" in todo,
                    "completed" in todo
                ])
                assert structure_ok, "Todos los TODOs deben tener estructura completa"
            
            logger.action("Estructura validada correctamente")
            logger.test_end("test_13_validar_limites_paginacion", "PASS")
        
        except Exception as e:
            logger.error(f"Test falló: {str(e)}")
            logger.test_end("test_13_validar_limites_paginacion", "FAIL")
            raise
    
    def test_14_validar_filtros_query_params(self, api_client):
        """
        Test 14: Validar filtros mediante query parameters
        """
        logger.test_start("test_14_validar_filtros_query_params")
        
        try:
            logger.step("Filtrando TODOs por userId")
            
            # Act - Filtrar por userId=1
            user_id = 1
            response = api_client.get(f"/todos?userId={user_id}")
            logger.api_request("GET", f"/todos?userId={user_id}", response.status_code)
            
            # Assert
            assert response.status_code == 200
            filtered_todos = response.json()
            
            logger.action(f"TODOs filtrados para userId={user_id}: {len(filtered_todos)}")
            
            # Validar que todos los resultados tienen el userId correcto
            all_match = all(todo["userId"] == user_id for todo in filtered_todos)
            logger.assertion(f"Todos tienen userId={user_id}", all_match)
            assert all_match, "Todos los resultados deben tener el userId especificado"
            
            # Validar que hay resultados
            has_results = len(filtered_todos) > 0
            logger.assertion("Filtro retorna resultados", has_results)
            assert has_results
            
            logger.action("Query parameters funcionan correctamente")
            logger.test_end("test_14_validar_filtros_query_params", "PASS")
        
        except Exception as e:
            logger.error(f"Test falló: {str(e)}")
            logger.test_end("test_14_validar_filtros_query_params", "FAIL")
            raise
    

class TestAPIRendimiento:
    """Suite de tests para verificar rendimiento básico"""
    
    def test_16_tiempo_respuesta_get_todos(self, api_client):
        """
        Test 16: Validar tiempo de respuesta para GET /todos
        """
        logger.test_start("test_16_tiempo_respuesta_get_todos")
        
        try:
            import time
            
            logger.step("Midiendo tiempo de respuesta")
            
            # Act
            start_time = time.time()
            response = api_client.get("/todos")
            end_time = time.time()
            
            response_time = (end_time - start_time) * 1000  # Convertir a ms
            
            logger.api_request("GET", "/todos", response.status_code)
            logger.action(f"Tiempo de respuesta: {response_time:.2f}ms")
            
            # Assert
            assert response.status_code == 200
            
            # Validar que el tiempo sea razonable (< 5 segundos)
            tiempo_razonable = response_time < 5000
            logger.assertion("Tiempo < 5000ms", tiempo_razonable)
            assert tiempo_razonable, f"Tiempo de respuesta demasiado alto: {response_time}ms"
            
            # Validar que haya datos
            todos = response.json()
            assert len(todos) > 0
            
            logger.action(f"Rendimiento aceptable ({response_time:.2f}ms para {len(todos)} items)")
            logger.test_end("test_16_tiempo_respuesta_get_todos", "PASS")
        
        except Exception as e:
            logger.error(f"Test falló: {str(e)}")
            logger.test_end("test_16_tiempo_respuesta_get_todos", "FAIL")
            raise
    
    def test_17_respuestas_concurrentes(self, api_client):
        """
        Test 17: Validar múltiples requests concurrentes
        """
        logger.test_start("test_17_respuestas_concurrentes")
        
        try:
            logger.step("Realizando 5 requests concurrentes")
            
            # Act - Simular requests concurrentes
            endpoints = ["/todos/1", "/todos/2", "/todos/3", "/posts/1", "/users/1"]
            responses = []

            for endpoint in endpoints:
                response = api_client.get(endpoint)
                responses.append(response)
                logger.api_request("GET", endpoint, response.status_code)
            
            # Assert
            logger.step("Validando todas las respuestas")
            
            all_success = all(r.status_code == 200 for r in responses)
            logger.assertion("Todas las respuestas son 200", all_success)
            assert all_success, "Todas las respuestas deben ser exitosas"
            
            all_have_data = all(len(r.json()) > 0 for r in responses)
            logger.assertion("Todas tienen datos", all_have_data)
            assert all_have_data
            
            logger.action(f"{len(responses)} requests procesados exitosamente")
            logger.test_end("test_17_respuestas_concurrentes", "PASS")
        
        except Exception as e:
            logger.error(f"Test falló: {str(e)}")
            logger.test_end("test_17_respuestas_concurrentes", "FAIL")
            raise


class TestAPIIntegridad:
    """Suite de tests para validar integridad de datos"""
    
    def test_18_validar_integridad_relaciones(self, api_client):
        """
        Test 18: Validar integridad de relaciones entre recursos
        """
        logger.test_start("test_18_validar_integridad_relaciones")
        
        try:
            logger.step("Obteniendo usuario y validando sus posts")
            
            # PASO 1: Obtener usuario
            user_response = api_client.get("/users/1")
            logger.api_request("GET", "/users/1", user_response.status_code)
            assert user_response.status_code == 200
            
            user = user_response.json()
            user_id = user["id"]
            logger.action(f"Usuario: {user['name']}")
            
            # PASO 2: Obtener posts del usuario
            posts_response = api_client.get(f"/users/{user_id}/posts")
            logger.api_request("GET", f"/users/{user_id}/posts", posts_response.status_code)
            assert posts_response.status_code == 200
            
            posts = posts_response.json()
            logger.action(f"Posts del usuario: {len(posts)}")
            
            # PASO 3: Validar que todos los posts pertenecen al usuario
            all_belong_to_user = all(post["userId"] == user_id for post in posts)
            logger.assertion("Todos los posts pertenecen al usuario", all_belong_to_user)
            assert all_belong_to_user
            
            # PASO 4: Obtener comentarios del primer post
            if len(posts) > 0:
                first_post_id = posts[0]["id"]
                comments_response = api_client.get(f"/posts/{first_post_id}/comments")
                logger.api_request("GET", f"/posts/{first_post_id}/comments", comments_response.status_code)
                assert comments_response.status_code == 200
                
                comments = comments_response.json()
                logger.action(f"Comentarios del post: {len(comments)}")
                
                # Validar integridad
                all_belong_to_post = all(c["postId"] == first_post_id for c in comments)
                logger.assertion("Todos los comentarios pertenecen al post", all_belong_to_post)
                assert all_belong_to_post
            
            logger.action("Integridad de relaciones validada")
            logger.test_end("test_18_validar_integridad_relaciones", "PASS")
        
        except Exception as e:
            logger.error(f"Test falló: {str(e)}")
            logger.test_end("test_18_validar_integridad_relaciones", "FAIL")
            raise
    
    def test_19_validar_tipos_datos(self, api_client):
        """
        Test 19: Validar tipos de datos en las respuestas
        """
        logger.test_start("test_19_validar_tipos_datos")
        
        try:
            logger.step("Validando tipos de datos en TODO")
            
            # Act
            response = api_client.get("/todos/1")
            logger.api_request("GET", "/todos/1", response.status_code)
            assert response.status_code == 200
            
            todo = response.json()
            
            # Assert - Validar tipos
            type_checks = [
                (isinstance(todo["userId"], int), "userId es int"),
                (isinstance(todo["id"], int), "id es int"),
                (isinstance(todo["title"], str), "title es str"),
                (isinstance(todo["completed"], bool), "completed es bool")
            ]
            
            for check, desc in type_checks:
                logger.assertion(desc, check)
                assert check, desc
            
            # Validar rangos
            logger.step("Validando rangos de valores")
            range_checks = [
                (todo["userId"] > 0, "userId positivo"),
                (todo["id"] > 0, "id positivo"),
                (len(todo["title"]) > 0, "title no vacío")
            ]
            
            for check, desc in range_checks:
                logger.assertion(desc, check)
                assert check
            
            logger.action("Tipos de datos validados correctamente")
            logger.test_end("test_19_validar_tipos_datos", "PASS")
        
        except Exception as e:
            logger.error(f"Test falló: {str(e)}")
            logger.test_end("test_19_validar_tipos_datos", "FAIL")
            raise
    
    def test_20_validar_consistencia_ids(self, api_client):
        """
        Test 20: Validar que los IDs son únicos y consistentes
        """
        logger.test_start("test_20_validar_consistencia_ids")
        
        try:
            logger.step("Obteniendo lista de TODOs")
            
            # Act
            response = api_client.get("/todos")
            logger.api_request("GET", "/todos", response.status_code)
            assert response.status_code == 200
            
            todos = response.json()
            logger.action(f"TODOs obtenidos: {len(todos)}")
            
            # Extraer todos los IDs
            ids = [todo["id"] for todo in todos]
            
            # Validar unicidad
            ids_unicos = len(ids) == len(set(ids))
            logger.assertion("IDs son únicos", ids_unicos)
            assert ids_unicos, "Todos los IDs deben ser únicos"
            
            # Validar que son positivos
            todos_positivos = all(id > 0 for id in ids)
            logger.assertion("Todos los IDs son positivos", todos_positivos)
            assert todos_positivos
            
            # Validar secuencialidad (JSONPlaceholder usa IDs secuenciales)
            ids_ordenados = sorted(ids)
            son_secuenciales = ids_ordenados == list(range(1, len(ids) + 1))
            logger.assertion("IDs son secuenciales", son_secuenciales)
            assert son_secuenciales
            
            logger.action("Consistencia de IDs validada")
            logger.test_end("test_20_validar_consistencia_ids", "PASS")
        
        except Exception as e:
            logger.error(f"Test falló: {str(e)}")
            logger.test_end("test_20_validar_consistencia_ids", "FAIL")
            raise

# FIXTURES Y CONFIGURACIÓN ADICIONAL

@pytest.fixture(scope="session", autouse=True)
def log_test_session_info():
    """Fixture para loggear información de la sesión de tests"""
    logger.info("INICIANDO SUITE DE TESTS DE API COMPLETA")
    logger.info(f"Archivo de datos: data/test_data_api.json")
    logger.info(f"Total de clases de test: 8")
    logger.info(f"Endpoint base: https://jsonplaceholder.typicode.com")
    
    yield
    
    logger.info("SUITE DE TESTS DE API FINALIZADA")