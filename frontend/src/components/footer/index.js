import styles from './style.module.css'
import { Container, LinkComponent } from '../index'

const Footer = () => {
  return <footer className={styles.footer}>
      <Container className={styles.footer__container}>
        <tr>
          <td><LinkComponent href='#' title='Продуктовый помощник' className={styles.footer__brand} /></td>
          <td><LinkComponent href='#' title='Технологии' className={styles.footer__link} /></td>
          <td><LinkComponent href='#' title='Об авторе' className={styles.footer__link} /></td>
        </tr>
      </Container>
  </footer>
}

export default Footer
