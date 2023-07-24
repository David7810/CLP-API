(define (domain sorting)
    (:requirements :typing)

    ;; type of object
    (:types esteira caracteristica
        item atuador - locatable
        atuador_duplo atuador_simples - atuador
        inicio fim - location
        location
        ;;incio box - location

    )
    ;;pequeno_nmetalico pequeno_metalico medio_nmetalico medio_metalico grande_nmetalico grande_metalico - caracteristica

    (:predicates
        ;; propriedades dos atuadores
        (extended ?atuador - atuador)
        (tipo ?s1 - atuador_simples ?c1 - caracteristica)

        ;; propriedades do atuador_duplo
        ;(retracted ?s - atuador_duplo)
        ;;(extended2 ?s - atuador_duplo)




        ;;propriedades da esteira
        (ligado ?e - esteira)



        (connected ?a - atuador ?c - caracteristica)
        ;;(connected2 ?ad - atuador_duplo ?c - caracteristica)

        (true1 ?c - caracteristica)


        (type ?i - item ?c - caracteristica)
        (at ?l - location ?i - locatable)

        (blocked ?e - esteira)
        (sorted ?i - item)

        (s_fimdecurso ?a - atuador)


        (link ?i - item ?i - item)
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
            (not (blocked ?e))
            (ligado ?e)
        )
        :effect (and
            (not (ligado ?e))
        )
    )

    (:action liga_avanco_atuador_simples
        :parameters (?as - atuador_simples ?c - caracteristica ?e - esteira ?l - location ?i - item ?x - inicio)
        :precondition (and
            (ligado ?e)
            (connected ?as ?c)
            (not (extended ?as))
            (at ?l ?as)
            (type ?i ?c)
            (not (blocked ?e))
            (not (sorted ?i))
            (at ?x ?i)
        )
        :effect (and
            (blocked ?e)
            (extended ?as)
            (at ?l ?i)
            (sorted ?i)
            (s_fimdecurso ?as)
            (ligado ?e)
        )
    )

    (:action desliga_avanco_atuador_simples
        :parameters (?as - atuador_simples ?e - esteira)
        :precondition (and
            (s_fimdecurso ?as)
            (extended ?as)
        )
        :effect (and
            (not (extended ?as))
            (not (blocked ?e))
            (not (s_fimdecurso ?as))
        )
    )


    (:action liga_avanco_atuador_duplo
        :parameters (?ad - atuador_duplo ?c - caracteristica ?e - esteira ?l - location ?i - item ?x - inicio)
        :precondition (and
            (ligado ?e)
            (connected ?ad ?c)
            (not (extended ?ad))
            (at ?l ?ad)
            (type ?i ?c)
            (not (blocked ?e))
            (not (sorted ?i))
            (at ?x ?i)
        )
        :effect (and
            (blocked ?e)
            (extended ?ad)
            (at ?l ?i)
            (sorted ?i)
            (s_fimdecurso ?ad)
            (ligado ?e)
        )
    )

    (:action desliga_avanco_atuador_duplo
        :parameters (?ad - atuador_duplo ?e - esteira)
        :precondition (and
            (s_fimdecurso ?ad)
            (extended ?ad)
        )
        :effect (and
            (not (extended ?ad))
	        (not (blocked ?e))
	        (not (s_fimdecurso ?ad))
        )
    )



    (:action next_link
        :parameters (?i - item ?f - item ?l - inicio)
        :precondition (and
            (link ?i ?f)
            (sorted ?i)
        )
        :effect (and
            (at ?l ?f)
        )
    )



)