from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Fornecedor(models.Model):
    nome_empresa = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.nome_empresa

class OpcaoDietetica(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Sorvete(models.Model):
    sabor = models.CharField(max_length=100)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='sorvetes/', blank=True, verbose_name='Foto do sabor')
    preco = models.DecimalField(max_digits=5, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    opcoes_dieteticas = models.ManyToManyField(OpcaoDietetica)

    def __str__(self):
        return self.sabor

class Comentario(models.Model):
    autor = models.CharField(max_length=100)
    email = models.EmailField()
    mensagem = models.TextField()

    def __str__(self):
        return f"Comentário sobre {self.autor} - {self.email}"


class Feedback(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    mensagem = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em', '-id']

    def __str__(self):
        return f"Feedback de {self.nome}"