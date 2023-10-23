from flask import Flask, jsonify, request, session
from bcrypt import gensalt, hashpw

app = Flask(__name__)
app.secret_key = 'chave_secreta'


conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='vieira1234',
    database='seboonline',
)

if conexao.is_connected():
    print("\nConexão ao MySQL bem-sucedida!\n")
    

### METÓDO POST PARA LOGIN DO USUÁRIO (VENDEDORES) ###
    @app.route('/items/login', methods=['POST'])
    def login_usuario_vendedor():
        
        login = request.get_json()
        
        usuario = login.get('name')
        senha = login.get('password')
        
        cursor = conexao.cursor()

        verificar_credenciais_sql = "SELECT iduser, name, password FROM user WHERE name = %s and type = vendedor"
        
        cursor.execute(verificar_credenciais_sql, (usuario,))
        
        resultado = cursor.fetchone()
        cursor.close()

        if resultado:
            # Verifique a senha criptografada usando bcrypt
            stored_password = resultado[2].encode('utf-8')
            
            if bcrypt.checkpw(senha.encode('utf-8'), stored_password):
                session['name'] = usuario

                response = {
                    'id': resultado[0],
                    'name': resultado[1],
                    'type': resultado[2]
                    'message': 'Login Feito com Sucesso!'
                }
                return jsonify(response)
        
        response = {
            'message': 'Dados Inválidos! Apenas Vendedores podem ter acesso.'
        }
        return jsonify(response)
########################################  


### METÓDO POST PARA LOGOUT DO USUÁRIO (VENDEDOR) ###
    @app.route('/items/logout', methods=['POST'])
    def logout_usuario_vendedor():
        if 'name' in session:
        
            session.pop('name', None)

            response = {
                'message': 'Usuário (Vendedor) acabou de sair da sessão!'
            }
            return jsonify(response)
        
        else:
            response = {
                'message': 'Nenhum Usuário (Vendedor) logado!'
            }
            return jsonify(response)
########################################    


### METÓDO POST PARA CRIAR ITENS ###
@app.route('/items', methods=['POST'])
def criar_itens():
    
        item = request.get_json()
        
        if 'title' in item and 'author' in item and 'category_id' in item
           'price' in item and 'description' in item and 'status' in item
           'date' in item and 'saller_id' in item:
        
            titulo          = item.get('title')
            autor           = item.get('author')
            categoria_id    = item.get('category_id')
            preco           = item.get('price')
            descricao       = item.get('description')
            status          = item.get('status')
            data            = item.get('date')
            vendedor_id     = item.get('saller_id')
            
            cursor = conexao.cursor()

            criar_item = f'INSERT INTO item (title, author, category_id, price, description, status, date, saller_id) 
                           VALUES ("{titulo}", "{autor}", "{categoria_id}", "{preco}", "{descricao}", "{status}", "{data}", "{vendedor_id}")' 
            cursor.execute(criar_item)

            conexao.commit()
            cursor.close()

               response = {
                'message': 'Categoria criado com sucesso!',
                'dados_user': criar_item
            }

            return jsonify(response)
        
        else:
            response = {
                'error': 'Verifique se os campos estão sendo inseridos corretamente!'
            }

            return jsonify(response)
########################################  


### METÓDO GET PARA LISTAR ITENS ###
    @app.route('/items', methods=['GET'])
    def mostrar_itens():
        
        if 'name' not in session:
            response = {
                'message': 'Realize o Login primeiro!'
            }
            return jsonify(response)
        
        cursor = conexao.cursor()
        
        recuperar_item_sql = "SELECT * FROM item"       
        cursor.execute(recuperar_item_sql)
        
        items = cursor.fetchall()
        cursor.close()

        item_json = [
            {
                'id'            : u[0], 
                'title'         : u[1], 
                'author'        : u[2], 
                'category_id'   : u[3], 
                'price'         : u[4], 
                'description'   : u[5],
                'status'        : u[6],
                'date'          : u[7],
                'saller_id'     : u[8]
            } 
            for u in items
        ]
        
        return jsonify(item_json)
######################################################


### METÓDO GET PARA LISTAR ITEM ESPECÍFICO ###
    @app.route('/items/<int:id>', methods=['GET'])
    def mostrar_item_especifico(id):
        
        if 'name' not in session:
            response = {
                'message': 'Realize o Login primeiro!'
            }
            return jsonify(response)
        
        cursor = conexao.cursor()
        
        recuperar_usuarios_sql = f'SELECT * FROM item WHERE iditem = "{id}"'       
        cursor.execute(recuperar_item_sql)
        
        items = cursor.fetchall()
        cursor.close()

        item_json = [
            {
                'id'            : u[0], 
                'title'         : u[1], 
                'author'        : u[2], 
                'category_id'   : u[3], 
                'price'         : u[4], 
                'description'   : u[5],
                'status'        : u[6],
                'date'          : u[7],
                'saller_id'     : u[8]
            } 
            for u in items
        ]
        
        return jsonify(item_json)
######################################################


### METÓDO PUT PARA EDITAR ITENS ###
    @app.route('/items/<int:id>', methods=['PUT'])
    def editar_item(id):
        
        if 'name' not in session:
            response = {
                'message': 'Realize o Login primeiro!'
            }
            return jsonify(response)
        
        editar_item = request.get_json()
        
        cursor = conexao.cursor()

        editar_item_sql = 'UPDATE item SET title = %s, author = %s, category_id = %s, price = %s, description = %s, status = %s,' 
                          'date = %s, saller_id = %s WHERE iditem = %s'
        
        cursor.execute(editar_item_sql, (
            editar_item['title'], 
            editar_item['author'], 
            editar_item['category_id'], 
            editar_item['price'],
            editar_item['description'],
            editar_item['status'],
            editar_item['date'],
            editar_item['saller_id'], 
            id
        ))

        conexao.commit()
        cursor.close()

        response = {
            'message': 'Item editado com sucesso!',
            'update_item': editar_item
        }
        return jsonify(response)
########################################


### METÓDO DEL PARA DELETAR USUÁRIOS ###
    @app.route('/items/<int:id>', methods=['DELETE'])
    def excluir_item(id):
    
        if 'name' not in session:
            response = {
                'message': 'Realize o Login primeiro!'
            }
            return jsonify(response)
    
        cursor = conexao.cursor()

        excluir_item_sql = "DELETE FROM item WHERE iditem = %s"  
        
        cursor.execute(excluir_usuario_sql, (id,))  

        conexao.commit()
        cursor.close()

        response = {
            'message': 'Item excluído com sucesso!'
        }
        return jsonify(response)
########################################     
        
else:
    print("Não foi possível conectar com o MySql!!")

app.run(port=5000, host='localhost', debug=True)