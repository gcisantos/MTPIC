
$(function () {



    var nodes = null;
    var edges = null;
    var network = null;
    var obj = null;


    $("#agrupaResultados").css("display", "none");
    $("#processarNovamente").css("display", "none");
    $("#dadosForumlario").css("display", "");

    $("#formaBusca").change(function () {
        switch ($("#formaBusca").val()) {
            case "Texto":
                $("#campos").html("<br><label for='texto'>Insira abaixo o texto que deseja realizar o processo de Lemmatization:</label>" +
                    "<textarea class='form-control' rows='5' id='texto' name='texto'></textarea>")
                break;
            case "Link": $("#campos").html("<br> <label for='link'>Insira o link que deseja processar</label> <input type='input' class='form-control' id='link' name='link' placeholder='Insira o link'>"); break;
            case "Arquivo": $("#campos").html("<br> <label for='arquivo'>Selecione o arquivo que deseja processar</label> <input type='file' class='form-control-file' name='arquivo' accept='.docx,.dotx,.pdf,.txt,.pptx,.jpg,.jpeg,.png,.jpe,.tif,.tiff,.bmp'>"); break;

        }
    });

    $("#novaBusca").click(function () {

        $("#formaBusca").val("nenhum");
        $("#campos").html("");
        $("#agrupaResultados").css("display", "none");
        $("#processarNovamente").css("display", "none");
        $("#dadosForumlario").css("display", "");
    });

    $("#processar").click(function () {


        var formaBusca = $("#formaBusca").val();
        processa = true
        switch (formaBusca) {
            case "Texto":
                break;
            case "Link":

                break;
            case "Arquivo":
                break;
            default: processa = false
        };



        if (processa) {



            $("body").css("cursor", "progress");
            $('#loading').modal({ backdrop: 'static', keyboard: false });
            var form = $('#formulario'),
                fd = new FormData(form[0]);
            $.ajax({
                url: '/processaTudo/',
                type: 'POST',
                contentType: false,
                processData: false,
                data: fd,
                dataType: 'json',
                timeout: 10000000,
                success: function (data) {

                   
                }
            }).done(function (data) {
                if (data.erro == "0") {
                    //Cria tabela com retorno do resultado
                    dados = data.tema.split(/\|@@##@@\|/g);

                    retorno = "<table class='table'><tr><th >Termo</th><th>Tema encotrado</th><th>Proximidade</th></tr>";

                    $.each(dados, function (index, linhas) {
                        colunas = linhas.replace(/\n/g, "").split(/\|@@#_#@@\|/g);

                        if (colunas[0] > 0) {
                            retorno += "<tr><td>" + colunas[0] + "</td><td>" + colunas[1].toString().replace("_", " ") + "</td><td>" + (parseFloat(colunas[2]) * 100).toFixed(3) + "%" + "</td></tr>";
                        }
                    });
                    retorno += "</table>";
                    $("#temaCentral").html(retorno);

                    dados = data.subTema.split(/\|@@##@@\|/g);

                    retorno = "<table class='table'><tr><th >Termo</th><th>Tema encotrado</th><th>Proximidade</th></tr>";

                    $.each(dados, function (index, linhas) {
                        colunas = linhas.replace(/\n/g, "").split(/\|@@#_#@@\|/g);

                        if (colunas[0] > 0) {
                            retorno += "<tr><td>" + colunas[0] + "</td><td>" + colunas[1].toString().replace("_", " ") + "</td><td>" + (parseFloat(colunas[2]) * 100).toFixed(3) + "%" + "</td></tr>";
                        }
                    });
                    retorno += "</table>";
                    $("#subTema").html(retorno);

                    montaGrafo(data.grafo.toString());



                    $("#agrupaResultados").css("display", "");
                    $("#processarNovamente").css("display", "");
                    $("#dadosForumlario").css("display", "none");
                }
                else {
                    alert("Não foi possivel processsar o texto inserido, tente de outra maneira.");
                }
                $('html, body').animate({ scrollTop: $('#agrupaResultados').offset().top }, 'slow');
                $("#loading").modal('hide');
                $("body").css("cursor", "default");

            });

        }
        else {
            alert("Selecione uma opção para processar");
        }
    });

    function montaGrafo(grafoJSON) {
        nodes = new vis.DataSet();

        edges = new vis.DataSet();
        obj = $.parseJSON(grafoJSON);


        $.each(obj, function (index, value) {
            nodes.add({ id: value.cod_titulo, value: (parseFloat(value.similaridade) * 100) * 1.5, label: value.titulo });

            conexoes = value.conexoes
            $.each(conexoes, function (subindex, subvalue) {
                edges.add({ id: value.cod_titulo + "_" + subvalue.cod_titulo, from: value.cod_titulo, to: subvalue.cod_titulo })

            });
        });


        // create connections between people
        // value corresponds with the amount of contact between two people


        // Instantiate our network object.
        var container = document.getElementById('mynetwork');
        var data = {
            nodes: nodes,
            edges: edges
        };

        if (nodes.length > 100) {
            options = {
                nodes: {
                    shape: 'dot',
                    scaling: {
                        min: 0,
                        max: 50
                    },
                    font: {
                        size: 12,
                        face: 'Tahoma',
                        color: "#e1e1e1"
                    },
                    color: { background: '#1e90ff', highlight: { background: '#70a1ff', border: 'rgb(225,225,225,0.85)' } }
                },
                edges: {
                    "smooth": false,
                    color: { color: '#AFAFAF', opacity: 0.4 },
                },
                "physics": {
                    "forceAtlas2Based": {
                        "gravitationalConstant": -13065,
                        "centralGravity": 0.005,
                        "springLength": 1480
                    },
                    "maxVelocity": 64,
                    "minVelocity": 0.75,
                    "solver": "forceAtlas2Based"
                }

            };
        }
        else {
            options = {
                nodes: {
                    shape: 'dot',
                    scaling: {
                        min: 3,
                        max: 8
                    },
                    font: {
                        size: 3,
                        face: 'Verdana',
                        color: "#e1e1e1"
                    },
                    color: { background: '#1e90ff', highlight: { background: '#70a1ff', border: 'rgb(225,225,225,0.85)' } }
                },
                edges: {
                    width: 0.15,
                    color: { color: '#AFAFAF', opacity: 0.4 },
                    smooth: {
                        type: 'continuous'
                    }
                },                
                interaction: {
                    tooltipDelay: 300,
                    hideEdgesOnDrag: true
                }
            };
        }

        network = new vis.Network(container, data, options);


        network.on("selectNode", clickNode);

        network.on("click", clickFora);

        network.on("doubleClick", duploClickNode);


    }

    function voltaCorPadrao() {
        nodesAtualizar = [];
        edgesAtualizar = [];

        nodes.forEach(function (parametro) {
            nodesAtualizar.push({ id: parametro.id, color: { background: '#1e90ff', border: '1e90ff', highlight: { background: '#70a1ff', border: 'rgb(225,225,225,0)' } }, font: { color: 'rgba(225, 225, 225,1)' } });

        });
        edges.forEach(function (parametro) {
            edgesAtualizar.push({ id: parametro.id, color: { color: '#AFAFAF', opacity: 0.4 } });

        });

        nodes.update(nodesAtualizar);
        edges.update(edgesAtualizar);
    }

    function invisibleNodes() {
        nodesAtualizar = [];
        edgesAtualizar = [];

        nodes.forEach(function (parametro) {
            nodesAtualizar.push({ id: parametro.id, color: { background: 'rgba(80,80,80,0.8)', border: 'rgba(80,80,80,0.15)' }, font: { color: 'rgba(80,80,80,0.15)' } })

        });
        edges.forEach(function (parametro) {
            edgesAtualizar.push({ id: parametro.id, color: { color: '#AFAFAF', opacity: 0 } })

        });

        nodes.update(nodesAtualizar);
        edges.update(edgesAtualizar);
    }

    function atualizaCorClicado(lista, clicado) {
        nodesAtualizar = [];
        edgesAtualizar = [];
        //Cria lista para atualizar
        $.each(lista[0].nodesRet, function (index, value) {
            nodesAtualizar.push({ id: value, color: { background: '#1e90ff', border: 'rgb(225,225,225,0.85)', highlight: { background: '#70a1ff', border: 'rgb(225,225,225,0.85)' } }, font: { color: 'rgba(225, 225, 225,1)' } })
        });

        $.each(lista[0].edgesRet, function (index, value) {
            edgesAtualizar.push({ id: value, color: { color: '#AFAFAF', opacity: 0.5 } })
        });


        nodes.update({ id: clicado, color: { background: '#1e90ff', border: 'rgb(225,225,225,0.85)', highlight: { background: '#70a1ff', border: 'rgb(225,225,225,0.85)' } }, font: { color: 'rgba(225, 225, 225,1)' } });
        nodes.update(nodesAtualizar);
        edges.update(edgesAtualizar);

    }

    function duploClickNode(params) {
        var id = this.getNodeAt(params.pointer.DOM);
        var items = nodes.get({
            filter: function (item) {
                return item.id == id;
            }

        });

        window.open("https://pt.wikipedia.org/wiki/" + encodeURIComponent(items[0].label));
    }

    function clickNode(params) {
        voltaCorPadrao();

        var id = this.getNodeAt(params.pointer.DOM);
        var items = nodes.get({
            filter: function (item) {
                return item.id == id;
            }
        });
        if (items.length > 0) {
            nodeClicado = obtemFilhosNode(items[0].id);
            //nodeClicado.push(items[0].id);
            invisibleNodes();
            atualizaCorClicado(nodeClicado, items[0].id);

        }
    }

    function clickFora(params) {
        var id = this.getNodeAt(params.pointer.DOM);
        var items = nodes.get({
            filter: function (item) {
                return item.id == id;
            }
        });
        if (items.length <= 0) {
            voltaCorPadrao();
        }
    }

    function obtemFilhosNode(id) {
        var retorno = [];
        var nodesRetorno = [];
        var edgeRetorno = [];
        $.each(obj, function (index, value) {
            conexoes = value.conexoes
            $.each(conexoes, function (subindex, subvalue) {
                if (value.cod_titulo == id) {
                    nodesRetorno.push(subvalue.cod_titulo);
                    edgeRetorno.push(value.cod_titulo + "_" + subvalue.cod_titulo);
                }
                if (subvalue.cod_titulo == id) {
                    nodesRetorno.push(value.cod_titulo);
                    edgeRetorno.push(value.cod_titulo + "_" + subvalue.cod_titulo);
                }
            });
        });
        retorno.push({ nodesRet: nodesRetorno, edgesRet: edgeRetorno });
        return retorno;
    }
});