(define (domain sorting)
    (:requirements :typing)

    (:types
        ;; tipos de objetos
        atuador_simples1 atuador_simples2 atuador_duplo1 - atuador
        grdmet medmet peqmet grdnmet mednmet peqnmet - objeto
        box1 box2 box3 - destination
        inicio destino - location
        esteira
        caracteristica
    )

    (:predicates
        ;;Estado do atuador
        (extended ?atuador - atuador)
        
        ;;Estado da esteira
        (ligado ?e - esteira)
        
        ;;Local do objeto
        (at ?o - objeto ?l - location)
        
        ;;Sensor de final de curso
        (s_fimdecurso ?a - atuador)
        
        ;;Tipo do objeto
        (type ?o - objeto ?c - caracteristica)
        
    )

    ;; ligar a esteira
    (:action ligar_esteira
        :parameters (?e - esteira)
        :precondition (and
            (not (ligado ?e))
        )
        :effect (and
            (ligado ?e)
        )
    )

    ;; desligar a esteira
    (:action desligar_esteira
        :parameters (?e - esteira)
        :precondition (and
            (ligado ?e)
        )
        :effect (and
            (not (ligado ?e))
        )
    )
    
    ;; Extende o atuador 1
    (:action extende_atuador1
        :parameters(?e - esteira ?a1 - atuador_simples1 ?a2 - atuador_simples2 ?a3 - atuador_duplo1 ?d - box1 ?i - inicio ?o - objeto ?c - caracteristica)
        :precondition (and
            (type ?o ?c)
            (ligado ?e)
            (not (extended ?a1))
            (not (extended ?a2))
            (not (extended ?a3))
            (at ?o ?i)
        )
        :effect (and
            (at ?o ?d)
            (not (at ?i ?d))
            (extended ?a1)
            (s_fimdecurso ?a1)
        )
    )
    
    ;; Extende o atuador 2
    (:action extende_atuador2
        :parameters(?e - esteira ?a1 - atuador_simples1 ?a2 - atuador_simples2 ?a3 - atuador_duplo1 ?d - box2 ?i - inicio ?o - objeto ?c - caracteristica)
        :precondition (and
            (type ?o ?c)
            (ligado ?e)
            (not (extended ?a1))
            (not (extended ?a2))
            (not (extended ?a3))
            (at ?o ?i)
        )
        :effect (and
            (at ?o ?d)
            (not (at ?i ?d))
            (extended ?a2)
            (s_fimdecurso ?a2)
        )
    )
    
    ;; Extende o atuador 3
    (:action extende_atuador3
        :parameters(?e - esteira ?a1 - atuador_simples1 ?a2 - atuador_simples2 ?a3 - atuador_duplo1 ?d - box3 ?i - inicio ?o - objeto ?c - caracteristica)
        :precondition (and
            (type ?o ?c)
            (ligado ?e)
            (not (extended ?a1))
            (not (extended ?a2))
            (not (extended ?a3))
            (at ?o ?i)
            )
        :effect (and
            (at ?o ?d)
            (not (at ?i ?d))
            (extended ?a3)
            (s_fimdecurso ?a3)
        )
    )
    
    ;; Retrai o atuador 1
    (:action retrai_atuador1
        :parameters(?a1 - atuador_simples1)
        :precondition (and
            (s_fimdecurso ?a1)
            (extended ?a1)
        )
        :effect (and
            (not (extended ?a1))
            (not (s_fimdecurso ?a1))
        )
    )
    
    ;; Retrai o atuador 2
    (:action retrai_atuador2
        :parameters(?a2 - atuador_simples2)
        :precondition (and
            (s_fimdecurso ?a2)
            (extended ?a2)
        )
        :effect (and
            (not (extended ?a2))
            (not (s_fimdecurso ?a2))
        )
    )
    
    ;; Retrai o atuador 3
    (:action retrai_atuador3
        :parameters(?a3 - atuador_duplo1)
        :precondition (and
            (s_fimdecurso ?a3)
            (extended ?a3)
        )
        :effect (and
            (not (extended ?a3))
            (not (s_fimdecurso ?a3))
        )
    )
)