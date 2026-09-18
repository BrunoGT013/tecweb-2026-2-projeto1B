from django.shortcuts import get_object_or_404, redirect, render

from .models import Note, Tag


def get_tags(texto):
    """Transforma o texto do campo de tags numa lista de objetos Tag.

    As tags vem separadas por virgula, entao 'comida, mercado' vira duas
    tags. A busca ignora maiusculas/minusculas para que 'Comida' e 'comida'
    nao virem duas tags diferentes no banco, e nomes repetidos entram so uma
    vez. Campo vazio significa nota sem nenhuma tag.
    """
    tags = []
    for name in (texto or '').split(','):
        name = name.strip()
        if not name:
            continue

        tag = Tag.objects.filter(name__iexact=name).first()
        if tag is None:
            tag = Tag.objects.create(name=name)
        if tag not in tags:
            tags.append(tag)
    return tags


def index(request):
    if request.method == 'POST':
        title = request.POST.get('titulo')
        content = request.POST.get('detalhes')
        note = Note.objects.create(title=title, content=content)
        note.tags.set(get_tags(request.POST.get('tags')))
        return redirect('index')
    else:
        all_notes = Note.objects.all()
        return render(request, 'notes/index.html', {'notes': all_notes})


def edit(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if request.method == 'POST':
        note.title = request.POST.get('titulo')
        note.content = request.POST.get('detalhes')
        note.save()
        note.tags.set(get_tags(request.POST.get('tags')))
        return redirect('index')
    else:
        tags_atuais = ', '.join(tag.name for tag in note.tags.all())
        return render(request, 'notes/edit.html', {'note': note, 'tags_atuais': tags_atuais})


def delete(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if request.method == 'POST':
        note.delete()
        return redirect('index')
    else:
        return render(request, 'notes/delete.html', {'note': note})


def tags(request):
    all_tags = Tag.objects.all()
    return render(request, 'notes/tags.html', {'tags': all_tags})


def tag_detail(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    return render(request, 'notes/tag_detail.html', {'tag': tag, 'notes': tag.notes.all()})
