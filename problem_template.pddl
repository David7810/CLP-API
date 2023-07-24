(define (problem more)
(:domain sorting)
    
    (:objects
        atuador_simples1 atuador_simples2 at_null - atuador_simples
        atuador_duplo1 - atuador_duplo
        esteira - esteira
        
        peqnmet peqmet mednmet medmet grdnmet grdmet - caracteristica
        
        item1 item2 item3 item4 item5 - item
        box1 box2 box3 - location
        inicio - inicio
        box4 - fim
    )
    
    (:init
        (connected atuador_simples1 grdmet)
        (connected atuador_simples1 peqnmet)
        
        (connected atuador_simples2 peqmet)
        (connected atuador_simples2 mednmet)
        
        (connected atuador_duplo1 medmet)
        (connected atuador_duplo1 grdnmet)
        

	;; Definir os itens
	
	;;
        
        
        ;; Definir item 1 no inicio

        ;;

	;; Definir a ordem

        ;;
        


        (at box1 atuador_simples1)
        (at box2 atuador_simples2)
        (at box3 atuador_duplo1)
        (at box4 at_null)
        
    )
    
    (:goal (and
        
	;; Definir a o destino

	;;
        
        (not (ligado esteira))
    ))
)